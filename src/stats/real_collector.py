"""Реальная реализация сборщика статистики из PostgreSQL."""

import logging
from datetime import datetime, timedelta
from typing import Any

import psycopg

from src.database import Database
from src.stats.collector import StatCollector
from src.stats.models import (
    DashboardStats,
    MessageStats,
    MetadataStats,
    OverviewStats,
    UserStats,
)

logger = logging.getLogger(__name__)


class RealStatCollector(StatCollector):
    """Реальная реализация StatCollector с данными из PostgreSQL."""

    def __init__(self, database: Database) -> None:
        """Инициализация сборщика статистики.

        Args:
            database: Экземпляр Database для работы с PostgreSQL
        """
        self.database = database
        logger.info("RealStatCollector initialized")

    async def get_dashboard_stats(self) -> DashboardStats:
        """Получение реальной статистики из БД.

        Returns:
            DashboardStats: Статистика для дашборда из PostgreSQL
        """
        conn = self.database._get_connection()
        try:
            with conn.cursor() as cur:
                # Общая статистика пользователей
                overview_stats = self._get_overview_stats(cur)

                # Статистика пользователей
                user_stats = self._get_user_stats(cur)

                # Статистика сообщений
                message_stats = self._get_message_stats(cur)

                # Метаданные
                metadata = MetadataStats(
                    generated_at=datetime.now(),
                    is_mock=False,
                )

                return DashboardStats(
                    overview=overview_stats,
                    users=user_stats,
                    messages=message_stats,
                    metadata=metadata,
                )
        finally:
            conn.close()

    def _get_overview_stats(self, cur: psycopg.Cursor[dict[str, Any]]) -> OverviewStats:
        """Получение общей статистики.

        Args:
            cur: Курсор базы данных

        Returns:
            OverviewStats: Общая статистика
        """
        # Общее количество пользователей
        cur.execute("SELECT COUNT(*) as count FROM users WHERE is_bot = FALSE")
        row = cur.fetchone()
        total_users = row["count"] if row else 0

        # Активные пользователи за 7 дней (хотя бы одно сообщение)
        seven_days_ago = datetime.now() - timedelta(days=7)
        cur.execute(
            """
            SELECT COUNT(DISTINCT m.user_id) as count
            FROM messages m
            JOIN users u ON m.user_id = u.user_id
            WHERE m.created_at >= %s
            AND m.deleted_at IS NULL
            AND u.is_bot = FALSE
            AND m.role = 'user'
            """,
            (seven_days_ago,),
        )
        row = cur.fetchone()
        active_users_7d = row["count"] if row else 0

        # Активные пользователи за 30 дней
        thirty_days_ago = datetime.now() - timedelta(days=30)
        cur.execute(
            """
            SELECT COUNT(DISTINCT m.user_id) as count
            FROM messages m
            JOIN users u ON m.user_id = u.user_id
            WHERE m.created_at >= %s
            AND m.deleted_at IS NULL
            AND u.is_bot = FALSE
            AND m.role = 'user'
            """,
            (thirty_days_ago,),
        )
        row = cur.fetchone()
        active_users_30d = row["count"] if row else 0

        # Общее количество сообщений (не удаленных)
        cur.execute(
            """
            SELECT COUNT(*) as count
            FROM messages
            WHERE deleted_at IS NULL
            """
        )
        row = cur.fetchone()
        total_messages = row["count"] if row else 0

        # Сообщения за 7 дней
        cur.execute(
            """
            SELECT COUNT(*) as count
            FROM messages
            WHERE created_at >= %s
            AND deleted_at IS NULL
            """,
            (seven_days_ago,),
        )
        row = cur.fetchone()
        messages_7d = row["count"] if row else 0

        # Сообщения за 30 дней
        cur.execute(
            """
            SELECT COUNT(*) as count
            FROM messages
            WHERE created_at >= %s
            AND deleted_at IS NULL
            """,
            (thirty_days_ago,),
        )
        row = cur.fetchone()
        messages_30d = row["count"] if row else 0

        return OverviewStats(
            total_users=total_users,
            active_users_7d=active_users_7d,
            active_users_30d=active_users_30d,
            total_messages=total_messages,
            messages_7d=messages_7d,
            messages_30d=messages_30d,
        )

    def _get_user_stats(self, cur: psycopg.Cursor[dict[str, Any]]) -> UserStats:
        """Получение статистики пользователей.

        Args:
            cur: Курсор базы данных

        Returns:
            UserStats: Статистика пользователей
        """
        # Количество Premium пользователей
        cur.execute(
            """
            SELECT COUNT(*) as count
            FROM users
            WHERE is_premium = TRUE AND is_bot = FALSE
            """
        )
        row = cur.fetchone()
        premium_count = row["count"] if row else 0

        # Количество обычных пользователей
        cur.execute(
            """
            SELECT COUNT(*) as count
            FROM users
            WHERE is_premium = FALSE AND is_bot = FALSE
            """
        )
        row = cur.fetchone()
        regular_count = row["count"] if row else 0

        # Процент Premium
        total_users = premium_count + regular_count
        premium_percentage = (
            round((premium_count / total_users) * 100, 2) if total_users > 0 else 0.0
        )

        # Распределение по языкам
        cur.execute(
            """
            SELECT
                COALESCE(language_code, 'unknown') as lang,
                COUNT(*) as count
            FROM users
            WHERE is_bot = FALSE
            GROUP BY language_code
            ORDER BY count DESC
            """
        )
        language_rows = cur.fetchall()

        # Формируем словарь языков
        by_language: dict[str, int] = {}
        for row in language_rows:
            lang = row["lang"]
            count = row["count"]

            # Группируем малочисленные языки в "other"
            if lang in ["ru", "en", "de", "unknown"]:
                by_language[lang] = count
            else:
                by_language["other"] = by_language.get("other", 0) + count

        # Убедимся, что хотя бы пустые значения есть для основных языков
        for lang in ["ru", "en", "de", "other", "unknown"]:
            if lang not in by_language:
                by_language[lang] = 0

        return UserStats(
            premium_count=premium_count,
            premium_percentage=premium_percentage,
            regular_count=regular_count,
            by_language=by_language,
        )

    def _get_message_stats(self, cur: psycopg.Cursor[dict[str, Any]]) -> MessageStats:
        """Получение статистики сообщений.

        Args:
            cur: Курсор базы данных

        Returns:
            MessageStats: Статистика сообщений
        """
        # Средняя длина сообщений
        cur.execute(
            """
            SELECT AVG(character_count) as avg_length
            FROM messages
            WHERE deleted_at IS NULL
            AND character_count > 0
            """
        )
        result = cur.fetchone()
        avg_length = (
            round(float(result["avg_length"]), 1) if result and result["avg_length"] else 0.0
        )

        # Дата первого сообщения
        cur.execute(
            """
            SELECT MIN(created_at) as first_date
            FROM messages
            WHERE deleted_at IS NULL
            """
        )
        result = cur.fetchone()
        first_message_date = (
            result["first_date"] if result and result["first_date"] else datetime.now()
        )

        # Дата последнего сообщения
        cur.execute(
            """
            SELECT MAX(created_at) as last_date
            FROM messages
            WHERE deleted_at IS NULL
            """
        )
        result = cur.fetchone()
        last_message_date = (
            result["last_date"] if result and result["last_date"] else datetime.now()
        )

        # Соотношение user/assistant сообщений
        cur.execute(
            """
            SELECT
                SUM(CASE WHEN role = 'user' THEN 1 ELSE 0 END) as user_count,
                SUM(CASE WHEN role = 'assistant' THEN 1 ELSE 0 END) as assistant_count
            FROM messages
            WHERE deleted_at IS NULL
            AND role IN ('user', 'assistant')
            """
        )
        result = cur.fetchone()
        user_count = result["user_count"] if result and result["user_count"] else 0
        assistant_count = result["assistant_count"] if result and result["assistant_count"] else 0

        user_to_assistant_ratio = (
            round(user_count / assistant_count, 2) if assistant_count > 0 else 0.0
        )

        return MessageStats(
            avg_length=avg_length,
            first_message_date=first_message_date,
            last_message_date=last_message_date,
            user_to_assistant_ratio=user_to_assistant_ratio,
        )
