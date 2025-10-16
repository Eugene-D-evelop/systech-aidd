<!-- 2b48152b-4cf5-4067-9ba6-48e2df8c2e9b a0476da9-cae8-4a1d-b13b-c092ee59ff12 -->
# Спринт S02: Реализация персистентного хранилища

## Обзор

Замена in-memory хранилища диалогов на персистентное хранение в PostgreSQL. Следуем принципу KISS - никакого ORM, простые SQL скрипты, прямые запросы через psycopg3.

## Новые возможности

- **Soft delete** - сообщения помечаются как удалённые, но физически не удаляются
- **Метаданные сообщений** - `created_at` (дата создания) и `character_count` (длина в символах) для каждого сообщения
- **PostgreSQL** - надёжное персистентное хранилище для production
- **Docker setup** - локальный PostgreSQL контейнер

## Этапы реализации

### 1. Настройка Docker

**Файл: `docker-compose.yml`** (новый)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: systech_aidd
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Файл: `.env.example`** (обновить)

- Добавить `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/systech_aidd`

### 2. Схема базы данных

**Файл: `migrations/001_create_messages.sql`** (новый)

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    character_count INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    CHECK (role IN ('user', 'assistant', 'system')),
    INDEX idx_chat_user (chat_id, user_id),
    INDEX idx_deleted (deleted_at)
);
```

Ключевые решения дизайна:

- `deleted_at` NULL = активное сообщение (стратегия soft delete)
- `character_count` предрасчитан для аналитики
- `created_at` для сортировки и отслеживания
- Индексы на `(chat_id, user_id)` для быстрого получения истории пользователя

### 3. Обновление конфигурации

**Файл: `src/config.py`**

Добавить конфигурацию базы данных:

```python
database_url: str = "postgresql://postgres:postgres@localhost:5432/systech_aidd"
database_timeout: int = 10
```

### 4. Слой работы с базой данных

**Файл: `src/database.py`** (новый)

Простой слой доступа к данным с использованием psycopg3:

```python
class Database:
    def __init__(self, connection_string: str, timeout: int):
        self.connection_string = connection_string
        self.timeout = timeout
        
    async def add_message(
        self, chat_id: int, user_id: int, role: str, content: str
    ) -> None:
        # INSERT с character_count = len(content)
        
    async def get_history(
        self, chat_id: int, user_id: int, limit: int | None = None
    ) -> list[dict[str, str]]:
        # SELECT WHERE deleted_at IS NULL
        # ORDER BY created_at
        # Возвращает только role + content (как в текущей реализации)
        
    async def clear_history(self, chat_id: int, user_id: int) -> None:
        # UPDATE messages SET deleted_at = NOW()
        # WHERE chat_id = ? AND user_id = ? AND deleted_at IS NULL
```

Ключевые моменты:

- Асинхронные операции с psycopg3
- Soft delete в `clear_history` (UPDATE, не DELETE)
- `character_count` рассчитывается автоматически
- Возвращает тот же формат, что и текущий класс `Conversation`

### 5. Рефакторинг Conversation

**Файл: `src/conversation.py`**

Заменить in-memory хранилище на вызовы базы данных:

```python
class Conversation:
    def __init__(self, database: Database) -> None:
        self.db = database
        
    async def add_message(...):
        await self.db.add_message(...)
        
    async def get_history(...):
        return await self.db.get_history(...)
        
    async def clear_history(...):
        await self.db.clear_history(...)
```

Удалить:

- `defaultdict` для in-memory хранилища
- поле `timestamp` (заменено на `created_at` в БД)
- метод `get_stats()` (можно добавить позже при необходимости)

### 6. Обновление зависимостей

**Файл: `pyproject.toml`**

Добавить в `dependencies`:

```toml
"psycopg[binary]>=3.1.0",
```

### 7. Runner для миграций

**Файл: `src/migrations.py`** (новый)

Простой скрипт для запуска SQL миграций:

```python
def run_migrations(database_url: str) -> None:
    conn = psycopg.connect(database_url)
    with open("migrations/001_create_messages.sql") as f:
        conn.execute(f.read())
    conn.commit()
```

Запускается один раз при старте или через команду `make migrate`.

### 8. Обновление главного приложения

**Файл: `src/main.py`**

- Инициализировать экземпляр `Database`
- Передать в `Conversation`
- Запустить миграции при старте (или проверить существование таблицы)

### 9. Обновление тестов

**Файл: `tests/test_conversation.py`**

Обновить тесты для работы с базой данных:

- Добавить pytest фикстуры с тестовой БД
- Использовать транзакции для изоляции тестов
- Сохранить ту же логику тестов, только с БД backend

**Файл: `tests/conftest.py`** (новый)

- Общие фикстуры для тестовой базы данных
- Логика setup/teardown

### 10. Обновление Makefile

Добавить команды:

```makefile
migrate:
    python -m src.migrations

db-up:
    docker compose up -d postgres

db-down:
    docker compose down
```

## Изменённые файлы

- **Новые:** `docker-compose.yml`, `migrations/001_create_messages.sql`, `src/database.py`, `src/migrations.py`, `tests/conftest.py`
- **Обновлённые:** `src/config.py`, `src/conversation.py`, `src/main.py`, `pyproject.toml`, `.env.example`, `Makefile`, `tests/test_conversation.py`

## Стратегия тестирования

1. Юнит-тесты для класса `Database` (с моками соединений)
2. Интеграционные тесты для `Conversation` с реальной тестовой БД
3. Проверка работы soft delete (удалённые сообщения не возвращаются)
4. Проверка корректного расчёта `character_count`
5. Проверка сортировки истории по `created_at`

## Критерии успеха

- ✅ Все существующие тесты проходят с БД backend
- ✅ История диалогов сохраняется между перезапусками бота
- ✅ `/reset` выполняет soft delete (помечает сообщения как удалённые)
- ✅ Каждое сообщение имеет `created_at` и `character_count`
- ✅ Отсутствует физическое удаление данных из базы
- ✅ Код следует принципу KISS (без ORM, простые запросы)
- ✅ Coverage остаётся на уровне 80%+

### To-dos

- [ ] Create docker-compose.yml for PostgreSQL and update .env.example
- [ ] Create migrations/001_create_messages.sql with messages table (soft delete, created_at, character_count)
- [ ] Add database_url and database_timeout to Config class
- [ ] Create src/database.py with Database class (add_message, get_history, clear_history)
- [ ] Create src/migrations.py to run SQL scripts
- [ ] Refactor src/conversation.py to use Database instead of in-memory storage
- [ ] Update src/main.py to initialize Database and run migrations
- [ ] Add psycopg[binary]>=3.1.0 to pyproject.toml
- [ ] Create tests/conftest.py with test database fixtures
- [ ] Update tests/test_conversation.py to work with database backend
- [ ] Add migrate, db-up, db-down commands to Makefile
- [ ] Run full test suite, verify persistence, soft delete, and metadata fields