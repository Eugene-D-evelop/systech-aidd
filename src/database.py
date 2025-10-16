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

