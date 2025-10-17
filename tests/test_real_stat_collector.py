"""Тесты для реального сборщика статистики из PostgreSQL."""

import pytest

from src.database import Database
from src.stats.real_collector import RealStatCollector


@pytest.mark.asyncio
async def test_real_stat_collector_basic(database: Database) -> None:
    """Тест базовой функциональности RealStatCollector.

    Args:
        database: Фикстура тестовой базы данных
    """
    # Создаем сборщик статистики
    collector = RealStatCollector(database)

    # Получаем статистику
    stats = await collector.get_dashboard_stats()

    # Проверяем, что данные получены
    assert stats is not None
    assert stats.metadata.is_mock is False
    assert stats.metadata.generated_at is not None

    # Проверяем основные метрики (могут быть 0 если БД пустая)
    assert stats.overview.total_users >= 0
    assert stats.overview.active_users_7d >= 0
    assert stats.overview.active_users_30d >= 0
    assert stats.overview.total_messages >= 0
    assert stats.overview.messages_7d >= 0
    assert stats.overview.messages_30d >= 0

    # Проверяем пользовательские данные
    assert stats.users.premium_count >= 0
    assert stats.users.regular_count >= 0
    assert 0 <= stats.users.premium_percentage <= 100
    assert isinstance(stats.users.by_language, dict)

    # Проверяем статистику сообщений
    assert stats.messages.avg_length >= 0
    assert stats.messages.first_message_date is not None
    assert stats.messages.last_message_date is not None
    assert stats.messages.user_to_assistant_ratio >= 0


@pytest.mark.asyncio
async def test_real_stat_collector_with_data(database: Database) -> None:
    """Тест RealStatCollector с реальными данными в БД.

    Args:
        database: Фикстура тестовой базы данных
    """
    test_user_id = 12345
    test_chat_id = 67890

    # Добавляем тестового пользователя
    await database.upsert_user(
        user_id=test_user_id,
        username="testuser",
        first_name="Test",
        last_name="User",
        language_code="ru",
        is_premium=True,
        is_bot=False,
    )

    # Добавляем тестовые сообщения
    await database.add_message(test_chat_id, test_user_id, "user", "Привет!")
    await database.add_message(
        test_chat_id, test_user_id, "assistant", "Здравствуйте!"
    )

    # Создаем сборщик и получаем статистику
    collector = RealStatCollector(database)
    stats = await collector.get_dashboard_stats()

    # Проверяем, что пользователь учтен
    assert stats.overview.total_users >= 1

    # Проверяем, что сообщения учтены
    assert stats.overview.total_messages >= 2

    # Проверяем, что есть Premium пользователь
    assert stats.users.premium_count >= 1
    assert stats.users.premium_percentage > 0

    # Проверяем, что русский язык присутствует
    assert "ru" in stats.users.by_language
    assert stats.users.by_language["ru"] >= 1

    # Проверяем, что средняя длина > 0 (есть сообщения)
    assert stats.messages.avg_length > 0

    # Проверяем соотношение user/assistant
    assert stats.messages.user_to_assistant_ratio > 0


@pytest.mark.asyncio
async def test_real_stat_collector_language_distribution(database: Database) -> None:
    """Тест распределения пользователей по языкам.

    Args:
        database: Фикстура тестовой базы данных
    """
    # Добавляем пользователей с разными языками
    await database.upsert_user(
        user_id=1001,
        username="user_ru",
        first_name="Russian",
        last_name="User",
        language_code="ru",
        is_premium=False,
        is_bot=False,
    )

    await database.upsert_user(
        user_id=1002,
        username="user_en",
        first_name="English",
        last_name="User",
        language_code="en",
        is_premium=False,
        is_bot=False,
    )

    await database.upsert_user(
        user_id=1003,
        username="user_de",
        first_name="German",
        last_name="User",
        language_code="de",
        is_premium=False,
        is_bot=False,
    )

    await database.upsert_user(
        user_id=1004,
        username="user_unknown",
        first_name="Unknown",
        last_name="User",
        language_code=None,
        is_premium=False,
        is_bot=False,
    )

    # Получаем статистику
    collector = RealStatCollector(database)
    stats = await collector.get_dashboard_stats()

    # Проверяем распределение языков
    assert "ru" in stats.users.by_language
    assert "en" in stats.users.by_language
    assert "de" in stats.users.by_language
    assert "unknown" in stats.users.by_language

    assert stats.users.by_language["ru"] >= 1
    assert stats.users.by_language["en"] >= 1
    assert stats.users.by_language["de"] >= 1
    assert stats.users.by_language["unknown"] >= 1

