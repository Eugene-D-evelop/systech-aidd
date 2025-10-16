"""Тесты для работы с пользователями в Database."""

import os
from datetime import datetime

import pytest

from src.database import Database

# Проверяем наличие DATABASE_URL для интеграционных тестов
pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL not set - skipping database tests",
)


@pytest.fixture
def db() -> Database:
    """Фикстура для создания экземпляра Database."""
    database_url = os.environ["DATABASE_URL"]
    return Database(database_url, timeout=10)


class TestUpsertUser:
    """Тесты для метода upsert_user."""

    async def test_upsert_user_creates_new_user(self, db: Database) -> None:
        """Тест создания нового пользователя."""
        user_id = 999000001
        username = "test_user"
        first_name = "Test"
        last_name = "User"
        language_code = "ru"
        is_premium = False
        is_bot = False

        # Создаем пользователя
        await db.upsert_user(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
            is_premium=is_premium,
            is_bot=is_bot,
        )

        # Проверяем что пользователь создан
        user = await db.get_user(user_id)
        assert user is not None
        assert user["user_id"] == user_id
        assert user["username"] == username
        assert user["first_name"] == first_name
        assert user["last_name"] == last_name
        assert user["language_code"] == language_code
        assert user["is_premium"] == is_premium
        assert user["is_bot"] == is_bot
        assert isinstance(user["created_at"], datetime)
        assert isinstance(user["updated_at"], datetime)

    async def test_upsert_user_updates_existing_user(self, db: Database) -> None:
        """Тест обновления существующего пользователя."""
        user_id = 999000002
        original_username = "original_user"
        updated_username = "updated_user"

        # Создаем пользователя
        await db.upsert_user(
            user_id=user_id,
            username=original_username,
            first_name="Original",
            last_name="Name",
            language_code="en",
            is_premium=False,
            is_bot=False,
        )

        # Получаем исходного пользователя
        original_user = await db.get_user(user_id)
        assert original_user is not None
        original_created_at = original_user["created_at"]

        # Обновляем пользователя
        await db.upsert_user(
            user_id=user_id,
            username=updated_username,
            first_name="Updated",
            last_name="Name",
            language_code="ru",
            is_premium=True,
            is_bot=False,
        )

        # Проверяем что данные обновились
        updated_user = await db.get_user(user_id)
        assert updated_user is not None
        assert updated_user["username"] == updated_username
        assert updated_user["first_name"] == "Updated"
        assert updated_user["language_code"] == "ru"
        assert updated_user["is_premium"] is True
        # created_at не должен измениться
        assert updated_user["created_at"] == original_created_at
        # updated_at должен обновиться
        assert updated_user["updated_at"] >= original_created_at

    async def test_upsert_user_with_null_values(self, db: Database) -> None:
        """Тест создания пользователя с NULL значениями."""
        user_id = 999000003

        # Создаем пользователя без username, last_name и language_code
        await db.upsert_user(
            user_id=user_id,
            username=None,
            first_name="Only",
            last_name=None,
            language_code=None,
            is_premium=False,
            is_bot=False,
        )

        # Проверяем что пользователь создан с NULL значениями
        user = await db.get_user(user_id)
        assert user is not None
        assert user["user_id"] == user_id
        assert user["username"] is None
        assert user["first_name"] == "Only"
        assert user["last_name"] is None
        assert user["language_code"] is None
        assert user["is_premium"] is False
        assert user["is_bot"] is False

    async def test_upsert_user_premium_user(self, db: Database) -> None:
        """Тест создания пользователя с Telegram Premium."""
        user_id = 999000004

        await db.upsert_user(
            user_id=user_id,
            username="premium_user",
            first_name="Premium",
            last_name="User",
            language_code="en",
            is_premium=True,
            is_bot=False,
        )

        user = await db.get_user(user_id)
        assert user is not None
        assert user["is_premium"] is True

    async def test_upsert_user_bot_account(self, db: Database) -> None:
        """Тест создания бота."""
        user_id = 999000005

        await db.upsert_user(
            user_id=user_id,
            username="test_bot",
            first_name="TestBot",
            last_name=None,
            language_code="en",
            is_premium=False,
            is_bot=True,
        )

        user = await db.get_user(user_id)
        assert user is not None
        assert user["is_bot"] is True


class TestGetUser:
    """Тесты для метода get_user."""

    async def test_get_user_existing(self, db: Database) -> None:
        """Тест получения существующего пользователя."""
        user_id = 999000010

        # Создаем пользователя
        await db.upsert_user(
            user_id=user_id,
            username="existing_user",
            first_name="Existing",
            last_name="User",
            language_code="en",
            is_premium=False,
            is_bot=False,
        )

        # Получаем пользователя
        user = await db.get_user(user_id)
        assert user is not None
        assert user["user_id"] == user_id
        assert user["username"] == "existing_user"

    async def test_get_user_not_found(self, db: Database) -> None:
        """Тест получения несуществующего пользователя."""
        user_id = 999999999

        # Пытаемся получить несуществующего пользователя
        user = await db.get_user(user_id)
        assert user is None


class TestGetUserStats:
    """Тесты для метода get_user_stats."""

    async def test_get_user_stats_with_messages(self, db: Database) -> None:
        """Тест получения статистики пользователя с сообщениями."""
        user_id = 999000020
        chat_id = 999000020

        # Создаем пользователя
        await db.upsert_user(
            user_id=user_id,
            username="stats_user",
            first_name="Stats",
            last_name="User",
            language_code="en",
            is_premium=False,
            is_bot=False,
        )

        # Добавляем несколько сообщений
        await db.add_message(chat_id, user_id, "user", "Hello")
        await db.add_message(chat_id, user_id, "assistant", "Hi there!")
        await db.add_message(chat_id, user_id, "user", "How are you?")

        # Получаем статистику
        stats = await db.get_user_stats(user_id)
        assert stats is not None
        assert stats["message_count"] == 2  # Только user сообщения
        assert stats["total_characters"] == 5 + 12  # "Hello" + "How are you?"
        assert stats["first_message_at"] is not None
        assert stats["last_message_at"] is not None
        assert isinstance(stats["first_message_at"], datetime)
        assert isinstance(stats["last_message_at"], datetime)

    async def test_get_user_stats_no_messages(self, db: Database) -> None:
        """Тест получения статистики пользователя без сообщений."""
        user_id = 999000021

        # Создаем пользователя
        await db.upsert_user(
            user_id=user_id,
            username="no_msg_user",
            first_name="NoMsg",
            last_name="User",
            language_code="en",
            is_premium=False,
            is_bot=False,
        )

        # Получаем статистику
        stats = await db.get_user_stats(user_id)
        assert stats is not None
        assert stats["message_count"] == 0
        assert stats["total_characters"] == 0
        assert stats["first_message_at"] is None
        assert stats["last_message_at"] is None

    async def test_get_user_stats_ignores_deleted_messages(self, db: Database) -> None:
        """Тест что статистика игнорирует удаленные сообщения."""
        user_id = 999000022
        chat_id = 999000022

        # Создаем пользователя
        await db.upsert_user(
            user_id=user_id,
            username="deleted_msg_user",
            first_name="Deleted",
            last_name="User",
            language_code="en",
            is_premium=False,
            is_bot=False,
        )

        # Добавляем сообщения
        await db.add_message(chat_id, user_id, "user", "Message 1")
        await db.add_message(chat_id, user_id, "user", "Message 2")

        # Удаляем историю (soft delete)
        await db.clear_history(chat_id, user_id)

        # Получаем статистику
        stats = await db.get_user_stats(user_id)
        assert stats is not None
        assert stats["message_count"] == 0  # Удаленные сообщения не считаются
        assert stats["total_characters"] == 0

    async def test_get_user_stats_nonexistent_user(self, db: Database) -> None:
        """Тест получения статистики несуществующего пользователя."""
        user_id = 999888888

        # Получаем статистику для несуществующего пользователя
        stats = await db.get_user_stats(user_id)
        assert stats is not None
        assert stats["message_count"] == 0
        assert stats["total_characters"] == 0
        assert stats["first_message_at"] is None
        assert stats["last_message_at"] is None

