"""Слой работы с базой данных."""

import logging
from typing import Any

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)


class Database:
    """Класс для работы с PostgreSQL через psycopg3."""

    def __init__(self, connection_string: str, timeout: int) -> None:
        """Инициализация подключения к базе данных.

        Args:
            connection_string: URL подключения к PostgreSQL
            timeout: Таймаут операций в секундах
        """
        self.connection_string = connection_string
        self.timeout = timeout
        logger.info("Database initialized")

    def _get_connection(self) -> psycopg.Connection[dict[str, Any]]:
        """Получение подключения к базе данных.

        Returns:
            Подключение к PostgreSQL
        """
        return psycopg.connect(
            self.connection_string,
            row_factory=dict_row,
            connect_timeout=self.timeout,
        )

    async def add_message(
        self, chat_id: int, user_id: int, role: str, content: str
    ) -> None:
        """Добавление сообщения в базу данных.

        Args:
            chat_id: ID чата
            user_id: ID пользователя
            role: Роль отправителя (user, assistant, system)
            content: Текст сообщения
        """
        character_count = len(content)

        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO messages (chat_id, user_id, role, content, character_count)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                (chat_id, user_id, role, content, character_count),
            )
            conn.commit()

        logger.debug(
            f"Message added for chat_id={chat_id}, user_id={user_id}, role={role}"
        )

    async def get_history(
        self, chat_id: int, user_id: int, limit: int | None = None
    ) -> list[dict[str, str]]:
        """Получение истории диалога пользователя.

        Args:
            chat_id: ID чата
            user_id: ID пользователя
            limit: Максимальное количество последних сообщений (None = все)

        Returns:
            Список сообщений в формате OpenAI API (только role и content)
        """
        with self._get_connection() as conn, conn.cursor() as cur:
            if limit is not None and limit > 0:
                cur.execute(
                    """
                        SELECT role, content
                        FROM messages
                        WHERE chat_id = %s AND user_id = %s AND deleted_at IS NULL
                        ORDER BY created_at ASC
                        LIMIT %s
                        """,
                    (chat_id, user_id, limit),
                )
            else:
                cur.execute(
                    """
                        SELECT role, content
                        FROM messages
                        WHERE chat_id = %s AND user_id = %s AND deleted_at IS NULL
                        ORDER BY created_at ASC
                        """,
                    (chat_id, user_id),
                )

            rows = cur.fetchall()

        # Возвращаем только role и content (без других полей)
        result = [{"role": row["role"], "content": row["content"]} for row in rows]

        logger.debug(
            f"Retrieved {len(result)} messages for chat_id={chat_id}, user_id={user_id}"
        )
        return result

    async def clear_history(self, chat_id: int, user_id: int) -> None:
        """Очистка истории диалога пользователя (soft delete).

        Args:
            chat_id: ID чата
            user_id: ID пользователя
        """
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    UPDATE messages
                    SET deleted_at = CURRENT_TIMESTAMP
                    WHERE chat_id = %s AND user_id = %s AND deleted_at IS NULL
                    """,
                (chat_id, user_id),
            )
            affected_rows = cur.rowcount
            conn.commit()

        logger.info(
            f"Soft deleted {affected_rows} messages for chat_id={chat_id}, user_id={user_id}"
        )

    async def upsert_user(
        self,
        user_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        language_code: str | None,
        is_premium: bool,
        is_bot: bool,
    ) -> None:
        """Создание или обновление информации о пользователе (UPSERT).

        Args:
            user_id: ID пользователя Telegram
            username: @username пользователя
            first_name: Имя пользователя
            last_name: Фамилия пользователя
            language_code: Код языка интерфейса
            is_premium: Наличие Telegram Premium
            is_bot: Является ли пользователь ботом
        """
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO users (
                        user_id, username, first_name, last_name,
                        language_code, is_premium, is_bot
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE SET
                        username = EXCLUDED.username,
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        language_code = EXCLUDED.language_code,
                        is_premium = EXCLUDED.is_premium,
                        is_bot = EXCLUDED.is_bot,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                (user_id, username, first_name, last_name, language_code, is_premium, is_bot),
            )
            conn.commit()

        logger.debug(f"User upserted: user_id={user_id}, username={username}")

    async def get_user(self, user_id: int) -> dict[str, Any] | None:
        """Получение информации о пользователе.

        Args:
            user_id: ID пользователя Telegram

        Returns:
            Словарь с информацией о пользователе или None, если не найден
        """
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    SELECT user_id, username, first_name, last_name,
                           language_code, is_premium, is_bot,
                           created_at, updated_at
                    FROM users
                    WHERE user_id = %s
                    """,
                (user_id,),
            )
            result = cur.fetchone()

        logger.debug(f"User retrieved: user_id={user_id}, found={result is not None}")
        return result

    async def get_user_stats(self, user_id: int) -> dict[str, Any]:
        """Получение статистики использования бота пользователем.

        Args:
            user_id: ID пользователя Telegram

        Returns:
            Словарь со статистикой (количество сообщений, символов и т.д.)
        """
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    SELECT
                        COUNT(*) as message_count,
                        SUM(character_count) as total_characters,
                        MIN(created_at) as first_message_at,
                        MAX(created_at) as last_message_at
                    FROM messages
                    WHERE user_id = %s AND role = 'user' AND deleted_at IS NULL
                    """,
                (user_id,),
            )
            result = cur.fetchone()

        # Преобразуем None в 0 для числовых полей
        if result:
            result["message_count"] = result["message_count"] or 0
            result["total_characters"] = result["total_characters"] or 0

        logger.debug(
            f"User stats retrieved: user_id={user_id}, "
            f"messages={result['message_count'] if result else 0}"
        )
        return result or {
            "message_count": 0,
            "total_characters": 0,
            "first_message_at": None,
            "last_message_at": None,
        }


