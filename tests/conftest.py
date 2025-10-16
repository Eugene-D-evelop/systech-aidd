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

    # Создаём таблицы для тестов
    with psycopg.connect(test_database_url) as conn:
        with conn.cursor() as cur:
            # Создаем таблицу users
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(255) NULL,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NULL,
                    language_code VARCHAR(10) NULL,
                    is_premium BOOLEAN NOT NULL DEFAULT FALSE,
                    is_bot BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Создаем таблицу messages
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
            """)
            
            # Создаем индексы
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_user ON messages (chat_id, user_id);
                CREATE INDEX IF NOT EXISTS idx_deleted ON messages (deleted_at);
                CREATE INDEX IF NOT EXISTS idx_users_username ON users (username) WHERE username IS NOT NULL;
                CREATE INDEX IF NOT EXISTS idx_users_created_at ON users (created_at);
            """)
            
            # Добавляем foreign key если его еще нет
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'fk_messages_user_id'
                    ) THEN
                        ALTER TABLE messages 
                        ADD CONSTRAINT fk_messages_user_id 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE;
                    END IF;
                END $$;
            """)
        conn.commit()

    yield db

    # Очищаем таблицы после тестов
    with psycopg.connect(test_database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE messages, users RESTART IDENTITY CASCADE")
        conn.commit()

