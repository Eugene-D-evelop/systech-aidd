"""Общие фикстуры для тестов."""

import psycopg
import pytest

from src.database import Database


@pytest.fixture
def test_database_url() -> str:
    """URL для тестовой базы данных."""
    return "postgresql://postgres:postgres@localhost:5433/systech_aidd_test"


@pytest.fixture
def database(test_database_url: str) -> Database:
    """Фикстура для создания экземпляра Database с тестовой БД."""
    db = Database(test_database_url, timeout=10)

    # Создаём таблицу для тестов
    with psycopg.connect(test_database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    chat_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    content TEXT NOT NULL,
                    character_count INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    deleted_at TIMESTAMP NULL,
                    CHECK (role IN ('user', 'assistant', 'system'))
                );

                CREATE INDEX IF NOT EXISTS idx_chat_user ON messages (chat_id, user_id);
                CREATE INDEX IF NOT EXISTS idx_deleted ON messages (deleted_at);
            """)
        conn.commit()

    yield db

    # Очищаем таблицу после тестов
    with psycopg.connect(test_database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE messages RESTART IDENTITY CASCADE")
        conn.commit()

