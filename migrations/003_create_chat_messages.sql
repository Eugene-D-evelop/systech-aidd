-- Migration: Create chat_messages table for web chat
-- Description: Table for storing web chat history (separate from Telegram bot messages)

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    sql_query TEXT NULL,  -- Only populated for admin mode responses
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for efficient session history retrieval
CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_messages(session_id, created_at);

-- Index for session lookup
CREATE INDEX IF NOT EXISTS idx_session_id ON chat_messages(session_id);

