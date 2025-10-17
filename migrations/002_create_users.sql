-- Создание таблицы users для хранения информации о пользователях Telegram
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

-- Индекс для поиска по username (только для пользователей с username)
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username) WHERE username IS NOT NULL;

-- Индекс для аналитики по дате регистрации
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users (created_at);

-- Комментарии к таблице и колонкам
COMMENT ON TABLE users IS 'Информация о пользователях Telegram бота';
COMMENT ON COLUMN users.user_id IS 'Уникальный ID пользователя из Telegram';
COMMENT ON COLUMN users.username IS '@username пользователя (может отсутствовать)';
COMMENT ON COLUMN users.first_name IS 'Имя пользователя (обязательное поле в Telegram)';
COMMENT ON COLUMN users.last_name IS 'Фамилия пользователя (опционально)';
COMMENT ON COLUMN users.language_code IS 'Код языка интерфейса (ru, en и т.д.)';
COMMENT ON COLUMN users.is_premium IS 'Наличие подписки Telegram Premium';
COMMENT ON COLUMN users.is_bot IS 'Является ли пользователь ботом';
COMMENT ON COLUMN users.created_at IS 'Дата и время первого взаимодействия с ботом';
COMMENT ON COLUMN users.updated_at IS 'Дата и время последнего обновления информации';

-- Создаем записи пользователей из существующих сообщений
-- Используем INSERT с ON CONFLICT для безопасного создания
INSERT INTO users (user_id, username, first_name, last_name, language_code, is_premium, is_bot)
SELECT DISTINCT 
    user_id,
    NULL as username,
    'User' as first_name,
    CAST(user_id AS VARCHAR) as last_name,
    NULL as language_code,
    FALSE as is_premium,
    FALSE as is_bot
FROM messages
WHERE user_id NOT IN (SELECT user_id FROM users)
ON CONFLICT (user_id) DO NOTHING;

-- Добавление foreign key от messages.user_id к users.user_id
-- Используем ON DELETE CASCADE для автоматического удаления сообщений при удалении пользователя
-- Проверяем, что constraint еще не существует
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'fk_messages_user_id'
    ) THEN
        ALTER TABLE messages 
        ADD CONSTRAINT fk_messages_user_id 
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id) 
        ON DELETE CASCADE;
    END IF;
END $$;

-- Индекс для foreign key (если не был создан автоматически)
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages (user_id);

