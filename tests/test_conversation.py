"""Тесты для модуля conversation с базой данных."""

import pytest

from src.conversation import Conversation
from src.database import Database


@pytest.fixture
def conversation(database: Database) -> Conversation:
    """Фикстура для создания Conversation с БД."""
    return Conversation(database)


@pytest.mark.asyncio
async def test_conversation_initialization(conversation: Conversation) -> None:
    """Тест инициализации Conversation."""
    assert conversation.db is not None


@pytest.mark.asyncio
async def test_add_message(conversation: Conversation, database: Database) -> None:
    """Тест добавления сообщения."""
    chat_id = 123
    user_id = 456

    # Создаем пользователя перед добавлением сообщения
    await database.upsert_user(user_id, "test_user", "Test", "User", "en", False, False)

    await conversation.add_message(chat_id, user_id, "user", "Hello")

    history = await conversation.get_history(chat_id, user_id)
    assert len(history) == 1
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"


@pytest.mark.asyncio
async def test_add_multiple_messages(conversation: Conversation, database: Database) -> None:
    """Тест добавления нескольких сообщений."""
    chat_id = 123
    user_id = 456

    # Создаем пользователя перед добавлением сообщений
    await database.upsert_user(user_id, "test_user", "Test", "User", "en", False, False)

    await conversation.add_message(chat_id, user_id, "user", "Hello")
    await conversation.add_message(chat_id, user_id, "assistant", "Hi there!")
    await conversation.add_message(chat_id, user_id, "user", "How are you?")

    history = await conversation.get_history(chat_id, user_id)
    assert len(history) == 3
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"
    assert history[2]["role"] == "user"


@pytest.mark.asyncio
async def test_get_history_with_limit(conversation: Conversation, database: Database) -> None:
    """Тест получения истории с лимитом."""
    chat_id = 123
    user_id = 456

    # Создаем пользователя
    await database.upsert_user(user_id, "test_user", "Test", "User", "en", False, False)

    # Добавляем 5 сообщений
    for i in range(5):
        await conversation.add_message(chat_id, user_id, "user", f"Message {i}")

    # Получаем последние 3 сообщения
    history = await conversation.get_history(chat_id, user_id, limit=3)
    assert len(history) == 3
    assert history[0]["content"] == "Message 0"
    assert history[1]["content"] == "Message 1"
    assert history[2]["content"] == "Message 2"


@pytest.mark.asyncio
async def test_get_history_no_limit(conversation: Conversation, database: Database) -> None:
    """Тест получения всей истории без лимита."""
    chat_id = 123
    user_id = 456

    # Создаем пользователя
    await database.upsert_user(user_id, "test_user", "Test", "User", "en", False, False)

    for i in range(5):
        await conversation.add_message(chat_id, user_id, "user", f"Message {i}")

    history = await conversation.get_history(chat_id, user_id)
    assert len(history) == 5


@pytest.mark.asyncio
async def test_get_history_empty(conversation: Conversation) -> None:
    """Тест получения истории для несуществующего пользователя."""
    history = await conversation.get_history(123, 456)
    assert history == []


@pytest.mark.asyncio
async def test_clear_history(conversation: Conversation, database: Database) -> None:
    """Тест очистки истории (soft delete)."""
    chat_id = 123
    user_id = 456

    # Создаем пользователя
    await database.upsert_user(user_id, "test_user", "Test", "User", "en", False, False)

    # Добавляем сообщения
    await conversation.add_message(chat_id, user_id, "user", "Hello")
    await conversation.add_message(chat_id, user_id, "assistant", "Hi!")

    # Проверяем что они есть
    history = await conversation.get_history(chat_id, user_id)
    assert len(history) == 2

    # Очищаем (soft delete)
    await conversation.clear_history(chat_id, user_id)

    # Проверяем что история пуста (удалённые не возвращаются)
    history = await conversation.get_history(chat_id, user_id)
    assert len(history) == 0


@pytest.mark.asyncio
async def test_clear_history_nonexistent(conversation: Conversation) -> None:
    """Тест очистки несуществующей истории."""
    # Не должно вызывать ошибок
    await conversation.clear_history(123, 456)


@pytest.mark.asyncio
async def test_multiple_users(conversation: Conversation, database: Database) -> None:
    """Тест работы с несколькими пользователями."""
    user1_chat = 123
    user1_id = 456

    user2_chat = 789
    user2_id = 101

    # Создаем обоих пользователей
    await database.upsert_user(user1_id, "user1", "User", "One", "en", False, False)
    await database.upsert_user(user2_id, "user2", "User", "Two", "en", False, False)

    # Добавляем сообщения для разных пользователей
    await conversation.add_message(user1_chat, user1_id, "user", "User 1 message")
    await conversation.add_message(user2_chat, user2_id, "user", "User 2 message")

    # Проверяем что истории не пересекаются
    history1 = await conversation.get_history(user1_chat, user1_id)
    history2 = await conversation.get_history(user2_chat, user2_id)

    assert len(history1) == 1
    assert len(history2) == 1
    assert history1[0]["content"] == "User 1 message"
    assert history2[0]["content"] == "User 2 message"


@pytest.mark.asyncio
async def test_message_format(conversation: Conversation, database: Database) -> None:
    """Тест формата сообщений (без timestamp и других полей в get_history)."""
    chat_id = 123
    user_id = 456

    # Создаем пользователя
    await database.upsert_user(user_id, "test_user", "Test", "User", "en", False, False)

    await conversation.add_message(chat_id, user_id, "user", "Test")

    history = await conversation.get_history(chat_id, user_id)
    message = history[0]

    # Проверяем что в возвращаемых сообщениях только role и content
    assert "role" in message
    assert "content" in message
    assert "timestamp" not in message
    assert "created_at" not in message
    assert "character_count" not in message


@pytest.mark.asyncio
async def test_user_key_generation(conversation: Conversation, database: Database) -> None:
    """Тест генерации уникальных ключей для пользователей."""
    # Создаем пользователей
    await database.upsert_user(456, "user1", "User", "One", "en", False, False)

    # Один пользователь в разных чатах - разные ключи
    await conversation.add_message(123, 456, "user", "Chat 1")
    await conversation.add_message(789, 456, "user", "Chat 2")

    history1 = await conversation.get_history(123, 456)
    history2 = await conversation.get_history(789, 456)

    assert len(history1) == 1
    assert len(history2) == 1
    assert history1[0]["content"] == "Chat 1"
    assert history2[0]["content"] == "Chat 2"


@pytest.mark.asyncio
async def test_character_count_calculation(conversation: Conversation, database: Database) -> None:
    """Тест расчета character_count при добавлении сообщения."""
    chat_id = 123
    user_id = 456
    content = "Test message with 25 chars"  # 27 символов

    # Создаем пользователя
    await database.upsert_user(user_id, "test_user", "Test", "User", "en", False, False)

    await conversation.add_message(chat_id, user_id, "user", content)

    # Проверяем напрямую в БД что character_count правильный
    import psycopg
    from psycopg.rows import dict_row

    with (
        psycopg.connect(database.connection_string, row_factory=dict_row) as conn,
        conn.cursor() as cur,
    ):
        cur.execute(
            "SELECT character_count FROM messages WHERE chat_id = %s AND user_id = %s",
            (chat_id, user_id),
        )
        row = cur.fetchone()
        assert row is not None
        assert row["character_count"] == len(content)


@pytest.mark.asyncio
async def test_soft_delete_persists_data(conversation: Conversation, database: Database) -> None:
    """Тест что soft delete не удаляет данные физически."""
    chat_id = 123
    user_id = 456

    # Создаем пользователя
    await database.upsert_user(user_id, "test_user", "Test", "User", "en", False, False)

    await conversation.add_message(chat_id, user_id, "user", "Test message")
    await conversation.clear_history(chat_id, user_id)

    # Проверяем что сообщение есть в БД, но с deleted_at
    import psycopg
    from psycopg.rows import dict_row

    with (
        psycopg.connect(database.connection_string, row_factory=dict_row) as conn,
        conn.cursor() as cur,
    ):
        cur.execute(
            "SELECT deleted_at FROM messages WHERE chat_id = %s AND user_id = %s",
            (chat_id, user_id),
        )
        row = cur.fetchone()
        assert row is not None
        assert row["deleted_at"] is not None  # Проверяем что deleted_at установлен
