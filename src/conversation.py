"""Управление контекстом и историей диалогов."""

import logging

from .database import Database

logger = logging.getLogger(__name__)


class Conversation:
    """Класс для управления историей диалогов пользователей через базу данных."""

    def __init__(self, database: Database) -> None:
        """Инициализация с подключением к базе данных.

        Args:
            database: Экземпляр Database для работы с БД
        """
        self.db = database
        logger.info("Conversation manager initialized with database backend")

    async def add_message(
        self, chat_id: int, user_id: int, role: str, content: str
    ) -> None:
        """Добавление сообщения в историю диалога.

        Args:
            chat_id: ID чата
            user_id: ID пользователя
            role: Роль отправителя (user, assistant, system)
            content: Текст сообщения
        """
        await self.db.add_message(chat_id, user_id, role, content)
        logger.debug(f"Message added for chat_id={chat_id}, user_id={user_id}, role={role}")

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
        history = await self.db.get_history(chat_id, user_id, limit)
        logger.debug(f"Retrieved {len(history)} messages for chat_id={chat_id}, user_id={user_id}")
        return history

    async def clear_history(self, chat_id: int, user_id: int) -> None:
        """Очистка истории диалога пользователя (soft delete).

        Args:
            chat_id: ID чата
            user_id: ID пользователя
        """
        await self.db.clear_history(chat_id, user_id)
        logger.info(f"History cleared for chat_id={chat_id}, user_id={user_id}")
