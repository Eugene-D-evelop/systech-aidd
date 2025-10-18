# Database Guide

Полное руководство по работе с PostgreSQL базой данных в проекте.

## Обзор

Проект использует **PostgreSQL 16** для персистентного хранения данных:
- История диалогов с Telegram ботом
- Информация о пользователях
- История веб-чата администратора

**Драйвер**: psycopg3 (чистый SQL, без ORM)

---

## Запуск базы данных

### Через Docker (рекомендуется)

```bash
# Запуск PostgreSQL контейнера
make db-up

# Остановка
make db-down
```

**Docker Compose конфигурация:**

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: systech-aidd-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: systech_aidd
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Локально (альтернатива)

Если PostgreSQL установлен локально:

```bash
# Создание базы данных
createdb -U postgres systech_aidd

# Подключение
psql -U postgres -d systech_aidd
```

---

## Схема базы данных

### Таблица `users`

Информация о пользователях Telegram.

```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    language_code VARCHAR(10),
    is_premium BOOLEAN NOT NULL DEFAULT FALSE,
    is_bot BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username) WHERE username IS NOT NULL;
CREATE INDEX idx_users_created_at ON users(created_at);
```

### Таблица `messages`

История диалогов с Telegram ботом.

```sql
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    character_count INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_messages_chat_user ON messages(chat_id, user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_deleted_at ON messages(deleted_at) WHERE deleted_at IS NULL;
```

### Таблица `chat_messages`

История веб-чата (админ панель).

```sql
CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    sql_query TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at);
```

---

## Миграции

### Структура миграций

Миграции хранятся в директории `migrations/`:

```
migrations/
├── 001_create_messages.sql
├── 002_create_users.sql
└── 003_create_chat_messages.sql
```

### Запуск миграций

Миграции выполняются автоматически при запуске бота:

```bash
# Бот автоматически выполнит миграции
make run

# Или вручную
uv run python -m src.migrations
```

**Логи миграций:**
```
2025-10-18 10:28:38,600 - src.migrations - INFO - Found 3 migration file(s)
2025-10-18 10:28:39,194 - src.migrations - INFO - Running migration: 001_create_messages.sql
2025-10-18 10:28:39,223 - src.migrations - INFO - Migration 001_create_messages.sql completed successfully
...
```

### Создание новой миграции

1. Создайте файл `migrations/00X_description.sql`
2. Напишите SQL команды
3. Миграция выполнится автоматически при следующем запуске

**Пример:**

```sql
-- migrations/004_add_user_preferences.sql
CREATE TABLE user_preferences (
    user_id BIGINT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    theme VARCHAR(10) DEFAULT 'dark',
    notifications BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Отслеживание миграций

Система автоматически создает таблицу `migrations_history`:

```sql
CREATE TABLE IF NOT EXISTS migrations_history (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL UNIQUE,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## Конфигурация

### Переменные окружения

**.env файл:**

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/systech_aidd
DATABASE_TIMEOUT=10
```

**Формат DATABASE_URL:**
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

### Config класс

```python
from src.config import Config

config = Config()
print(config.database_url)      # postgresql://...
print(config.database_timeout)  # 10
```

---

## Использование в коде

### Database класс

```python
from src.database import Database
from src.config import Config

config = Config()
db = Database(config.database_url, config.database_timeout)

# Сохранение сообщения
await db.add_message(
    chat_id=123456789,
    user_id=123456789,
    role="user",
    content="Привет!"
)

# Получение истории
history = await db.get_history(
    chat_id=123456789,
    user_id=123456789,
    limit=10
)

# Soft delete
await db.clear_history(
    chat_id=123456789,
    user_id=123456789
)

# UPSERT пользователя
await db.upsert_user(
    user_id=123456789,
    username="test_user",
    first_name="Test",
    last_name="User",
    language_code="ru",
    is_premium=False,
    is_bot=False
)
```

### Conversation класс

Высокоуровневая обертка над Database:

```python
from src.conversation import Conversation
from src.database import Database
from src.config import Config

config = Config()
db = Database(config.database_url, config.database_timeout)
conversation = Conversation(db)

# Те же методы, что и у Database
await conversation.add_message(...)
history = await conversation.get_history(...)
await conversation.clear_history(...)
```

---

## Особенности реализации

### Soft-delete

Вместо физического удаления используется soft-delete через `deleted_at`:

```python
# Удаление (soft)
UPDATE messages 
SET deleted_at = CURRENT_TIMESTAMP 
WHERE chat_id = 123 AND user_id = 456;

# Выборка только активных
SELECT * FROM messages 
WHERE deleted_at IS NULL;
```

**Преимущества:**
- Возможность восстановления
- Аудит и аналитика
- GDPR compliance

### UPSERT стратегия

Для пользователей используется UPSERT:

```sql
INSERT INTO users (user_id, username, first_name, ...)
VALUES (123, 'test', 'Test', ...)
ON CONFLICT (user_id) DO UPDATE SET
    username = EXCLUDED.username,
    first_name = EXCLUDED.first_name,
    updated_at = CURRENT_TIMESTAMP;
```

Автоматическое создание или обновление при каждом взаимодействии.

### Чистый SQL (без ORM)

Проект не использует ORM (SQLAlchemy, Django ORM и т.д.):
- ✅ Простота и прозрачность
- ✅ Полный контроль над SQL
- ✅ Легкая отладка
- ✅ Высокая производительность

---

## Типичные SQL запросы

### Статистика пользователей

```sql
-- Всего пользователей (не боты)
SELECT COUNT(*) FROM users WHERE is_bot = FALSE;

-- Premium пользователи
SELECT COUNT(*) FROM users 
WHERE is_premium = TRUE AND is_bot = FALSE;

-- Распределение по языкам
SELECT language_code, COUNT(*) as count
FROM users
WHERE is_bot = FALSE
GROUP BY language_code
ORDER BY count DESC;
```

### Статистика сообщений

```sql
-- Всего сообщений
SELECT COUNT(*) FROM messages WHERE deleted_at IS NULL;

-- Активные пользователи за 7 дней
SELECT COUNT(DISTINCT m.user_id)
FROM messages m
JOIN users u ON m.user_id = u.user_id
WHERE m.created_at >= NOW() - INTERVAL '7 days'
  AND m.deleted_at IS NULL
  AND u.is_bot = FALSE
  AND m.role = 'user';

-- Средняя длина сообщения
SELECT AVG(character_count)
FROM messages
WHERE deleted_at IS NULL AND character_count > 0;
```

### Очистка старых данных

```sql
-- Удаление сообщений старше 90 дней
UPDATE messages
SET deleted_at = CURRENT_TIMESTAMP
WHERE created_at < NOW() - INTERVAL '90 days'
  AND deleted_at IS NULL;

-- Физическое удаление старых soft-deleted
DELETE FROM messages
WHERE deleted_at < NOW() - INTERVAL '180 days';
```

---

## Backup и Restore

### Создание backup

```bash
# Полный backup
docker exec systech-aidd-postgres-1 pg_dump -U postgres systech_aidd > backup.sql

# Только схема
docker exec systech-aidd-postgres-1 pg_dump -U postgres -s systech_aidd > schema.sql

# Только данные
docker exec systech-aidd-postgres-1 pg_dump -U postgres -a systech_aidd > data.sql
```

### Восстановление

```bash
# Из backup файла
docker exec -i systech-aidd-postgres-1 psql -U postgres systech_aidd < backup.sql

# Пересоздание БД
docker exec systech-aidd-postgres-1 dropdb -U postgres systech_aidd
docker exec systech-aidd-postgres-1 createdb -U postgres systech_aidd
docker exec -i systech-aidd-postgres-1 psql -U postgres systech_aidd < backup.sql
```

---

## Мониторинг

### Проверка подключения

```bash
# Через psql
docker exec -it systech-aidd-postgres-1 psql -U postgres -d systech_aidd

# Через Python
uv run python -c "from src.database import Database; from src.config import Config; db = Database(Config().database_url, 10); print('Connected!')"
```

### Размер базы данных

```sql
-- Размер БД
SELECT pg_size_pretty(pg_database_size('systech_aidd'));

-- Размер таблиц
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Активные соединения

```sql
SELECT count(*) FROM pg_stat_activity 
WHERE datname = 'systech_aidd';
```

---

## Troubleshooting

### Проблема: БД не запускается

```bash
# Проверка логов
docker logs systech-aidd-postgres-1

# Проверка портов
netstat -ano | findstr :5433

# Пересоздание контейнера
docker compose down
docker volume rm systech-aidd_postgres_data
docker compose up -d postgres
```

### Проблема: Ошибка подключения

```python
# Проверка DATABASE_URL
from src.config import Config
print(Config().database_url)

# Тест подключения
import psycopg
conn = psycopg.connect("postgresql://postgres:postgres@localhost:5433/systech_aidd")
print("Connected!")
```

### Проблема: Миграции не применяются

```bash
# Проверка таблицы миграций
docker exec -it systech-aidd-postgres-1 psql -U postgres -d systech_aidd -c "SELECT * FROM migrations_history;"

# Ручное применение
docker exec -i systech-aidd-postgres-1 psql -U postgres -d systech_aidd < migrations/001_create_messages.sql
```

---

## Best Practices

### 1. Используйте параметризованные запросы

```python
# ✅ Хорошо (защита от SQL injection)
cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))

# ❌ Плохо (SQL injection риск)
cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
```

### 2. Всегда используйте транзакции

```python
with db._get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("UPDATE users ...")
        conn.commit()  # Явный commit
```

### 3. Используйте индексы

```sql
-- Для часто используемых WHERE условий
CREATE INDEX idx_messages_chat_user ON messages(chat_id, user_id);

-- Для partial indexes
CREATE INDEX idx_active_messages ON messages(chat_id) WHERE deleted_at IS NULL;
```

### 4. Мониторьте производительность

```sql
-- Медленные запросы
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;
```

---

## Что дальше?

- [Architecture Overview](02_ARCHITECTURE_OVERVIEW.md) - общая архитектура
- [Data Model](03_DATA_MODEL.md) - структуры данных
- [Configuration](06_CONFIGURATION_AND_SECRETS.md) - настройка конфигурации
- [Development Workflow](08_DEVELOPMENT_WORKFLOW.md) - процесс разработки

---

**Версия:** 1.0  
**Дата создания:** 2025-10-18  
**Статус:** Актуально

