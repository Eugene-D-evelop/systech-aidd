"""Управление контекстом и историей диалогов."""

import logging
import time

logger = logging.getLogger(__name__)


class Conversation:
    """Класс для управления историей диалогов пользователей."""

    def __init__(self):
        """Инициализация хранилища диалогов."""
        self.conversations: dict[str, list[dict]] = {}
        logger.info("Conversation storage initialized")

    def _get_user_key(self, chat_id: int, user_id: int) -> str:
        """Формирование ключа для пользователя.

        Args:
            chat_id: ID чата
            user_id: ID пользователя

        Returns:
            Строковый ключ формата "chat_id:user_id"
        """
        return f"{chat_id}:{user_id}"

    def add_message(self, chat_id: int, user_id: int, role: str, content: str) -> None:
        """Добавление сообщения в историю диалога.

        Args:
            chat_id: ID чата
            user_id: ID пользователя
            role: Роль отправителя (user, assistant, system)
            content: Текст сообщения
        """
        user_key = self._get_user_key(chat_id, user_id)

        if user_key not in self.conversations:
            self.conversations[user_key] = []

        message = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
        }

        self.conversations[user_key].append(message)
        logger.debug(f"Message added for {user_key}, role: {role}")

    def get_history(
        self, chat_id: int, user_id: int, limit: int | None = None
    ) -> list[dict]:
        """Получение истории диалога пользователя.

        Args:
            chat_id: ID чата
            user_id: ID пользователя
            limit: Максимальное количество последних сообщений (None = все)

        Returns:
            Список сообщений в формате OpenAI API (без timestamp)
        """
        user_key = self._get_user_key(chat_id, user_id)

        if user_key not in self.conversations:
            logger.debug(f"No history found for {user_key}")
            return []

        messages = self.conversations[user_key]

        # Применяем лимит, если указан
        if limit is not None and limit > 0:
            messages = messages[-limit:]

        # Возвращаем только role и content (без timestamp)
        result = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        logger.debug(f"Retrieved {len(result)} messages for {user_key}")
        return result

    def clear_history(self, chat_id: int, user_id: int) -> None:
        """Очистка истории диалога пользователя.

        Args:
            chat_id: ID чата
            user_id: ID пользователя
        """
        user_key = self._get_user_key(chat_id, user_id)

        if user_key in self.conversations:
            message_count = len(self.conversations[user_key])
            self.conversations[user_key] = []
            logger.info(f"Cleared {message_count} messages for {user_key}")
        else:
            logger.debug(f"No history to clear for {user_key}")

    def get_stats(self) -> dict[str, int]:
        """Получение статистики по диалогам.

        Returns:
            Словарь со статистикой (количество пользователей, сообщений)
        """
        total_users = len(self.conversations)
        total_messages = sum(len(msgs) for msgs in self.conversations.values())

        return {
            "total_users": total_users,
            "total_messages": total_messages,
        }

