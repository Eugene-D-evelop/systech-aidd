-- Создание таблицы messages с поддержкой soft delete
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

-- Индекс для быстрого поиска истории пользователя
CREATE INDEX IF NOT EXISTS idx_chat_user ON messages (chat_id, user_id);

-- Индекс для фильтрации по deleted_at
CREATE INDEX IF NOT EXISTS idx_deleted ON messages (deleted_at);


