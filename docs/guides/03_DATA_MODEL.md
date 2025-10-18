# Data Model

Понимание структур данных и их жизненного цикла в проекте.

## Config - Конфигурация приложения

### Структура

```python
class Config(BaseSettings):
    # Обязательные параметры
    telegram_bot_token: str
    openrouter_api_key: str
    openrouter_model: str
    system_prompt: str
    
    # Опциональные параметры с дефолтами
    max_history_length: int = 10
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 60
    
    # База данных
    database_url: str = "postgresql://postgres:postgres@localhost:5433/systech_aidd"
    database_timeout: int = 10
```

### Параметры

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `telegram_bot_token` | str | ✅ | Токен Telegram бота от @BotFather |
| `openrouter_api_key` | str | ✅ | API ключ OpenRouter |
| `openrouter_model` | str | ✅ | Модель LLM (например, `openai/gpt-4o-mini`) |
| `system_prompt` | str | ✅ | Системный промпт, определяющий роль бота |
| `max_history_length` | int | ❌ | Лимит сообщений в истории (default: 10) |
| `temperature` | float | ❌ | Креативность LLM 0.0-2.0 (default: 0.7) |
| `max_tokens` | int | ❌ | Максимум токенов в ответе (default: 1000) |
| `timeout` | int | ❌ | Таймаут API запросов в секундах (default: 60) |
| `database_url` | str | ❌ | URL подключения к PostgreSQL (default: localhost:5433) |
| `database_timeout` | int | ❌ | Таймаут подключения к БД в секундах (default: 10) |

### Особенности

- **Pydantic BaseSettings** - автоматическая валидация типов
- **Загрузка из .env** - через `SettingsConfigDict`
- **Валидация при старте** - падает с ошибкой если обязательные поля отсутствуют
- **Immutable** - конфигурация не меняется после инициализации

### Пример в .env

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
OPENROUTER_API_KEY=sk-or-v1-abcdef1234567890
OPENROUTER_MODEL=openai/gpt-4o-mini
SYSTEM_PROMPT=Ты - Python Code Reviewer. Анализируешь Python код, находишь баги, предлагаешь улучшения.
MAX_HISTORY_LENGTH=10
TEMPERATURE=0.7
MAX_TOKENS=1000
TIMEOUT=60
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/systech_aidd
DATABASE_TIMEOUT=10
```

## Message - Структура сообщения

### Формат

```python
{
    "role": str,         # "user" | "assistant" | "system"
    "content": str,      # Текст сообщения
    "timestamp": float   # Unix timestamp (time.time())
}
```

### Поля

| Поле | Тип | Значения | Описание |
|------|-----|----------|----------|
| `role` | str | `user`, `assistant`, `system` | Роль отправителя |
| `content` | str | любой текст | Содержимое сообщения |
| `timestamp` | float | Unix timestamp | Время создания сообщения |

### Жизненный цикл

```mermaid
graph LR
    USER[User отправляет<br/>текст в Telegram]
    ADD[Conversation.<br/>add_message]
    STORE[In-memory storage<br/>с timestamp]
    GET[Conversation.<br/>get_history]
    FILTER[Фильтрация<br/>удаление timestamp]
    LLM[Отправка в<br/>LLMClient]
    
    USER --> ADD
    ADD --> STORE
    STORE --> GET
    GET --> FILTER
    FILTER --> LLM
    
    style USER fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#fff
    style STORE fill:#c05621,stroke:#dd6b20,stroke-width:2px,color:#fff
    style LLM fill:#6b46c1,stroke:#805ad5,stroke-width:2px,color:#fff
```

### Примеры

**User message:**
```python
{
    "role": "user",
    "content": "def hello():\n  print('hi')",
    "timestamp": 1729098000.123
}
```

**Assistant message:**
```python
{
    "role": "assistant",
    "content": "Найдены замечания:\n1. Отступ должен быть 4 пробела...",
    "timestamp": 1729098003.456
}
```

**System message (промпт):**
```python
{
    "role": "system",
    "content": "Ты - Python Code Reviewer. Анализируешь Python код...",
    "timestamp": 1729098000.000
}
```

## Database Schema - Схема базы данных

### Технология

**PostgreSQL 16** через **psycopg3** драйвер

### Таблицы

#### Таблица `users`

Хранение информации о пользователях Telegram.

| Колонка | Тип | Описание |
|---------|-----|----------|
| `user_id` | BIGINT PRIMARY KEY | ID пользователя Telegram |
| `username` | VARCHAR(255) | @username (может быть NULL) |
| `first_name` | VARCHAR(255) | Имя пользователя |
| `last_name` | VARCHAR(255) | Фамилия (может быть NULL) |
| `language_code` | VARCHAR(10) | Код языка (ru, en, и т.д.) |
| `is_premium` | BOOLEAN | Наличие Telegram Premium |
| `is_bot` | BOOLEAN | Является ли пользователь ботом |
| `created_at` | TIMESTAMPTZ | Дата первого взаимодействия |
| `updated_at` | TIMESTAMPTZ | Дата последнего обновления |

#### Таблица `messages`

Хранение истории диалогов с ботом.

| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | BIGSERIAL PRIMARY KEY | Уникальный ID сообщения |
| `chat_id` | BIGINT | ID чата Telegram |
| `user_id` | BIGINT → users | ID пользователя (foreign key) |
| `role` | VARCHAR(20) | Роль: user, assistant, system |
| `content` | TEXT | Текст сообщения |
| `character_count` | INTEGER | Количество символов |
| `created_at` | TIMESTAMPTZ | Время создания сообщения |
| `deleted_at` | TIMESTAMPTZ | Время удаления (NULL = не удалено) |

#### Таблица `chat_messages`

Хранение истории веб-чата (админ панель).

| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | BIGSERIAL PRIMARY KEY | Уникальный ID сообщения |
| `session_id` | VARCHAR(255) | ID сессии веб-чата |
| `role` | VARCHAR(20) | Роль: user, assistant |
| `content` | TEXT | Текст сообщения |
| `sql_query` | TEXT | SQL запрос (только для admin mode) |
| `created_at` | TIMESTAMPTZ | Время создания сообщения |

### Ключ пользователя

Формат идентификации: `"chat_id:user_id"`

**Примеры**:
- Личный чат: `"123456789:123456789"`
- Групповой чат: `"987654321:123456789"` (разные пользователи имеют разные истории)

### Схема данных

```mermaid
erDiagram
    USERS ||--o{ MESSAGES : creates
    USERS {
        bigint user_id PK
        varchar username
        varchar first_name
        varchar last_name
        varchar language_code
        boolean is_premium
        boolean is_bot
        timestamptz created_at
        timestamptz updated_at
    }
    MESSAGES {
        bigserial id PK
        bigint chat_id
        bigint user_id FK
        varchar role
        text content
        integer character_count
        timestamptz created_at
        timestamptz deleted_at
    }
    CHAT_MESSAGES {
        bigserial id PK
        varchar session_id
        varchar role
        text content
        text sql_query
        timestamptz created_at
    }
```

### Пример SQL запроса

```sql
-- Получение истории диалога пользователя
SELECT role, content
FROM messages
WHERE chat_id = 123456789 
  AND user_id = 123456789 
  AND deleted_at IS NULL
ORDER BY created_at ASC
LIMIT 10;
```

## Операции с данными

### Добавление сообщения

```python
conversation.add_message(
    chat_id=123456789,
    user_id=111111,
    role="user",
    content="Проверь этот код"
)
```

**Что происходит**:
1. Формируется ключ: `"123456789:111111"`
2. Создается message с timestamp
3. Добавляется в `conversations[key]`
4. `defaultdict` автоматически создает список для новых пользователей

### Получение истории

```python
history = conversation.get_history(
    chat_id=123456789,
    user_id=111111,
    limit=10  # Последние 10 сообщений
)
```

**Что происходит**:
1. Формируется ключ: `"123456789:111111"`
2. Извлекаются последние N сообщений
3. **Фильтруется timestamp** - возвращается только `role` и `content`
4. Формат готов для отправки в LLM API

**Результат**:
```python
[
    {"role": "user", "content": "Привет!"},
    {"role": "assistant", "content": "Здравствуйте!"}
]
```

### Очистка истории

```python
conversation.clear_history(
    chat_id=123456789,
    user_id=111111
)
```

Удаляет все сообщения для пользователя. Используется при команде `/reset`.

### Ограничение истории

```mermaid
graph LR
    FULL["Полная история<br/>20 сообщений"]
    LIMIT["Применение лимита<br/>max_history_length=10"]
    RECENT["Последние 10<br/>сообщений"]
    LLM["Отправка в LLM<br/>(экономия токенов)"]
    
    FULL --> LIMIT
    LIMIT --> RECENT
    RECENT --> LLM
    
    style FULL fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#fff
    style LIMIT fill:#744210,stroke:#975a16,stroke-width:2px,color:#fff
    style RECENT fill:#2f855a,stroke:#38a169,stroke-width:2px,color:#fff
    style LLM fill:#6b46c1,stroke:#805ad5,stroke-width:2px,color:#fff
```

## Системный промпт (System Prompt)

### Назначение

Системный промпт определяет **роль и поведение** бота. Это ключевой элемент ролевой модели AI-продукта.

### Текущий промпт

```
Ты - Python Code Reviewer. 
Анализируешь Python код, находишь баги, предлагаешь улучшения. 
Работаешь только с Python, не пишешь код за пользователя.
```

### Использование

Системный промпт передается в LLM API как первое сообщение с `role: "system"`:

```python
messages = [
    {"role": "system", "content": config.system_prompt},
    {"role": "user", "content": "def hello():\n  print('hi')"},
]
```

### Влияние на поведение

| Элемент промпта | Эффект |
|-----------------|--------|
| "Ты - Python Code Reviewer" | Определяет роль и специализацию |
| "Анализируешь Python код" | Описывает основную функцию |
| "Работаешь только с Python" | Устанавливает границы (ограничения) |
| "Не пишешь код за пользователя" | Определяет стиль ответов |

## Особенности модели данных

### PostgreSQL persistence

**Преимущества**:
- ✅ Персистентное хранение (данные сохраняются между перезапусками)
- ✅ Масштабируемость (может работать с множеством экземпляров бота)
- ✅ Транзакции и ACID гарантии
- ✅ Индексы для быстрого поиска
- ✅ Foreign keys для целостности данных

**Особенности реализации**:
- Используем чистый SQL через psycopg3 (без ORM для простоты)
- Soft-delete стратегия (`deleted_at IS NULL`)
- SQL миграции для версионирования схемы

### Soft-delete

Вместо физического удаления используется soft-delete:

```sql
-- Вместо DELETE
UPDATE messages 
SET deleted_at = CURRENT_TIMESTAMP 
WHERE chat_id = 123 AND user_id = 456;

-- Выборка только активных
SELECT * FROM messages 
WHERE deleted_at IS NULL;
```

**Преимущества**:
- ✅ Возможность восстановления данных
- ✅ Аудит и аналитика удаленных сообщений
- ✅ Соответствие требованиям GDPR (можно полностью удалить позже)

### Timestamps и метаданные

Все таблицы имеют временные метки:
- `created_at` - время создания записи
- `updated_at` (только users) - время последнего обновления
- `deleted_at` (messages) - время удаления (NULL = активна)

Данные метки используются для:
- Сортировки истории диалогов
- Аналитики активности пользователей
- Очистки старых данных

## Что дальше?

- [Architecture Overview](02_ARCHITECTURE_OVERVIEW.md) - общая архитектура
- [🎨 Архитектурная визуализация](../architecture_visualization.md) - диаграммы Data Flow и Storage Structure
- [Integrations](04_INTEGRATIONS.md) - работа с внешними API
- [Configuration](06_CONFIGURATION_AND_SECRETS.md) - настройка конфигурации

