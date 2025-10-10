"""Тесты для модуля conversation."""

import time

import pytest

from src.conversation import Conversation


@pytest.fixture
def conversation():
    """Фикстура для создания Conversation."""
    return Conversation()


def test_conversation_initialization(conversation):
    """Тест инициализации Conversation."""
    assert conversation.conversations == {}
    stats = conversation.get_stats()
    assert stats["total_users"] == 0
    assert stats["total_messages"] == 0


def test_add_message(conversation):
    """Тест добавления сообщения."""
    chat_id = 123
    user_id = 456

    conversation.add_message(chat_id, user_id, "user", "Hello")

    history = conversation.get_history(chat_id, user_id)
    assert len(history) == 1
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"


def test_add_multiple_messages(conversation):
    """Тест добавления нескольких сообщений."""
    chat_id = 123
    user_id = 456

    conversation.add_message(chat_id, user_id, "user", "Hello")
    conversation.add_message(chat_id, user_id, "assistant", "Hi there!")
    conversation.add_message(chat_id, user_id, "user", "How are you?")

    history = conversation.get_history(chat_id, user_id)
    assert len(history) == 3
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"
    assert history[2]["role"] == "user"


def test_get_history_with_limit(conversation):
    """Тест получения истории с лимитом."""
    chat_id = 123
    user_id = 456

    # Добавляем 5 сообщений
    for i in range(5):
        conversation.add_message(chat_id, user_id, "user", f"Message {i}")

    # Получаем последние 3 сообщения
    history = conversation.get_history(chat_id, user_id, limit=3)
    assert len(history) == 3
    assert history[0]["content"] == "Message 2"
    assert history[1]["content"] == "Message 3"
    assert history[2]["content"] == "Message 4"


def test_get_history_no_limit(conversation):
    """Тест получения всей истории без лимита."""
    chat_id = 123
    user_id = 456

    for i in range(5):
        conversation.add_message(chat_id, user_id, "user", f"Message {i}")

    history = conversation.get_history(chat_id, user_id)
    assert len(history) == 5


def test_get_history_empty(conversation):
    """Тест получения истории для несуществующего пользователя."""
    history = conversation.get_history(123, 456)
    assert history == []


def test_clear_history(conversation):
    """Тест очистки истории."""
    chat_id = 123
    user_id = 456

    # Добавляем сообщения
    conversation.add_message(chat_id, user_id, "user", "Hello")
    conversation.add_message(chat_id, user_id, "assistant", "Hi!")

    # Проверяем что они есть
    assert len(conversation.get_history(chat_id, user_id)) == 2

    # Очищаем
    conversation.clear_history(chat_id, user_id)

    # Проверяем что история пуста
    assert len(conversation.get_history(chat_id, user_id)) == 0


def test_clear_history_nonexistent(conversation):
    """Тест очистки несуществующей истории."""
    # Не должно вызывать ошибок
    conversation.clear_history(123, 456)


def test_multiple_users(conversation):
    """Тест работы с несколькими пользователями."""
    user1_chat = 123
    user1_id = 456

    user2_chat = 789
    user2_id = 101

    # Добавляем сообщения для разных пользователей
    conversation.add_message(user1_chat, user1_id, "user", "User 1 message")
    conversation.add_message(user2_chat, user2_id, "user", "User 2 message")

    # Проверяем что истории не пересекаются
    history1 = conversation.get_history(user1_chat, user1_id)
    history2 = conversation.get_history(user2_chat, user2_id)

    assert len(history1) == 1
    assert len(history2) == 1
    assert history1[0]["content"] == "User 1 message"
    assert history2[0]["content"] == "User 2 message"


def test_get_stats(conversation):
    """Тест получения статистики."""
    conversation.add_message(123, 456, "user", "Hello")
    conversation.add_message(123, 456, "assistant", "Hi")
    conversation.add_message(789, 101, "user", "Test")

    stats = conversation.get_stats()
    assert stats["total_users"] == 2
    assert stats["total_messages"] == 3


def test_message_format(conversation):
    """Тест формата сообщений (без timestamp в get_history)."""
    chat_id = 123
    user_id = 456

    conversation.add_message(chat_id, user_id, "user", "Test")

    history = conversation.get_history(chat_id, user_id)
    message = history[0]

    # Проверяем что в возвращаемых сообщениях только role и content
    assert "role" in message
    assert "content" in message
    assert "timestamp" not in message


def test_user_key_generation(conversation):
    """Тест генерации уникальных ключей для пользователей."""
    # Один пользователь в разных чатах - разные ключи
    conversation.add_message(123, 456, "user", "Chat 1")
    conversation.add_message(789, 456, "user", "Chat 2")

    history1 = conversation.get_history(123, 456)
    history2 = conversation.get_history(789, 456)

    assert len(history1) == 1
    assert len(history2) == 1
    assert history1[0]["content"] == "Chat 1"
    assert history2[0]["content"] == "Chat 2"

