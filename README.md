# systech-aidd

LLM-ассистент в виде Telegram-бота через OpenRouter API

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![Coverage](https://img.shields.io/badge/coverage-81%25-brightgreen.svg)](https://github.com/pytest-dev/pytest-cov)

## 🚀 Быстрый старт

### Предварительные требования

- **Python 3.11+**
- **uv** - менеджер зависимостей ([установка](https://github.com/astral-sh/uv))
- **Docker** - для PostgreSQL базы данных ([установка](https://docs.docker.com/get-docker/))

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/systech-aidd.git
cd systech-aidd
```

2. Установите зависимости:
```bash
make install
```

3. Создайте `.env` файл на основе примера:
```bash
cp .env.example .env
```

4. Заполните `.env` своими ключами:
```env
# Telegram Bot Token от @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenRouter API Key
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=openai/gpt-oss-20b:free

# LLM Параметры
TEMPERATURE=0.7
MAX_TOKENS=1000
TIMEOUT=60

# Настройки бота
SYSTEM_PROMPT=Ты полезный AI-ассистент. Отвечай кратко и по существу.
MAX_HISTORY_LENGTH=10

# База данных
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/systech_aidd
DATABASE_TIMEOUT=10
```

5. Запустите PostgreSQL:
```bash
make db-up
```

6. Примените миграции базы данных:
```bash
make migrate
```

### Запуск бота

```bash
make run
```

Бот автоматически применит миграции при запуске и начнет обрабатывать сообщения.

## 📋 Команды разработки

### Основные команды

```bash
# Установка зависимостей
make install          # uv sync

# База данных
make db-up            # Запустить PostgreSQL в Docker
make db-down          # Остановить PostgreSQL
make migrate          # Применить миграции

# Запуск бота
make run              # uv run python -m src.main

# Форматирование кода
make format           # ruff format src/ tests/

# Проверка кода
make lint             # ruff check + mypy (strict mode)

# Тестирование
make test             # Все тесты + coverage (HTML отчет)
make test-unit        # Только юнит-тесты (не требуют .env)
make test-integration # Только интеграционные тесты

# CI/CD проверка
make ci               # lint + test-unit
```

### API сервер (Mock)

```bash
# Запуск API сервера для frontend разработки
make api-dev             # Запуск в dev режиме с auto-reload

# Тестирование API
make api-test            # Проверка работоспособности через curl

# Документация API
make api-docs            # Открыть Swagger UI (http://localhost:8000/docs)
```

**Примеры запросов:**
```bash
# Health check
curl http://localhost:8000/health

# Получение статистики
curl http://localhost:8000/api/stats/dashboard

# С форматированием
curl http://localhost:8000/api/stats/dashboard | python -m json.tool
```

> 📖 **Подробнее:** [Tasklist F01](docs/tasklists/tasklist-F01.md) - Mock API для дашборда статистики

### Frontend (Dashboard) 🆕

```bash
# Запуск frontend dev server (требует Node.js 18+ и pnpm)
cd frontend
pnpm install             # Установка зависимостей (первый раз)
pnpm dev                 # Запуск dev server (localhost:3000)

# Или из корня проекта через Makefile
make frontend-install    # Установка зависимостей
make frontend-dev        # Запуск dev server

# Проверка качества кода
make frontend-lint       # ESLint
make frontend-format     # Prettier
make frontend-type-check # TypeScript
```

**Полный запуск (API + Frontend):**
```bash
# Terminal 1: Mock API
make api-dev

# Terminal 2: Frontend
make frontend-dev

# Откройте http://localhost:3000/dashboard
```

> 📖 **Подробнее:** 
> - [Frontend README](frontend/README.md) - документация frontend проекта
> - [Frontend Roadmap](docs/frontend-roadmap.md) - спринты F01-F05
> - [Sprint F03 Summary](docs/tasklists/sprint-F03-summary.md) - реализация Dashboard

### Перед коммитом

Всегда запускайте:
```bash
make ci
```

Эта команда выполнит:
- ✅ Проверку ruff (линтер)
- ✅ Проверку mypy (типизация)
- ✅ Юнит-тесты с coverage

## 🏗️ Архитектура

Проект следует принципам **KISS** и **ООП** с минимальными абстракциями:

```
src/
├── main.py           # Точка входа для Telegram бота
├── api_main.py       # Точка входа для API сервера
├── config.py         # Pydantic конфигурация из .env
├── bot.py            # Инициализация Telegram бота
├── handlers.py       # Обработчики сообщений + error handling
├── llm_client.py     # Клиент OpenRouter API + исключения
├── conversation.py   # Менеджер истории диалогов (PostgreSQL)
├── database.py       # Подключение и работа с PostgreSQL
├── migrations.py     # Система миграций базы данных
├── stats/            # Модуль статистики
│   ├── collector.py      # Абстрактный интерфейс StatCollector
│   ├── models.py         # Pydantic модели для API response
│   └── mock_collector.py # Mock реализация (для разработки frontend)
└── api/              # REST API модуль
    └── app.py            # FastAPI приложение

migrations/
├── 001_create_messages.sql  # Создание таблицы messages
└── 002_create_users.sql     # Создание таблицы users
```

> 📊 **Визуальное представление:** См. [Архитектурная визуализация](docs/architecture_visualization.md) - 12 диаграмм Mermaid с разных точек зрения (C4, Sequence, State, Data Flow и др.)

### Ключевые особенности

- ✅ **Строгая типизация** - mypy strict mode, 100% typed
- ✅ **SRP** - разделение ответственности (error handling в handlers)
- ✅ **Async/await** - для всех I/O операций
- ✅ **Независимые тесты** - юнит-тесты не требуют .env
- ✅ **Относительные импорты** - правильная структура модулей
- ✅ **PostgreSQL** - постоянное хранение истории диалогов и профилей пользователей
- ✅ **Soft Delete** - безопасное удаление с сохранением данных
- ✅ **Миграции** - автоматическое управление схемой БД
- ✅ **User Management** - автоматическое сохранение информации о пользователях

## 🧪 Тестирование

### Запуск тестов

```bash
# Только юнит-тесты (быстро, не требуют .env)
make test-unit

# Все тесты с coverage
make test

# Только интеграционные тесты
make test-integration
```

### Метрики покрытия

| Модуль | Coverage | Статус |
|--------|----------|--------|
| `config.py` | 100% | ✅ |
| `conversation.py` | 100% | ✅ |
| `handlers.py` | 100% | ✅ |
| `bot.py` | 100% | ✅ |
| `database.py` | 100% | ✅ |
| `llm_client.py` | 80% | ✅ |
| `main.py` | 0% | ⚠️ |
| `migrations.py` | 0% | ⚠️ |
| **Всего** | **69%** | ✅ |

**Цель достигнута!** 🎉 Покрытие для основных модулей 100%

## 📦 Технологии

### Основной стек

- **Python 3.11+** - язык разработки
- **uv** - управление зависимостями
- **aiogram 3.x** - Telegram Bot API (async, polling)
- **openai** - SDK для OpenRouter API
- **pydantic** - валидация конфигурации и моделей данных
- **PostgreSQL 16** - хранение истории диалогов
- **psycopg 3** - async драйвер для PostgreSQL
- **FastAPI** - REST API для статистики (Mock реализация)
- **Uvicorn** - ASGI сервер для FastAPI
- **Docker** - контейнеризация БД

### Инструменты качества

- **ruff** - линтер и форматтер (правила: E, F, I, N, W, B, C4, UP, SIM, RET, ARG)
- **mypy** - статическая проверка типов (strict mode)
- **pytest** + **pytest-asyncio** - тестирование
- **pytest-cov** - измерение покрытия кода

## 🤖 Использование бота

> **Роль бота:** Python Code Reviewer - эксперт по проверке и улучшению Python кода

### Команды

- `/start` - Запуск бота и приветствие (персонализированное)
- `/role` - Отображение роли и специализации бота
- `/reset` - Сброс истории диалога
- `/me` - **✨ НОВОЕ** Просмотр своего профиля и статистики

### Ролевая специализация

Бот работает как **Python Code Reviewer** и специализируется на:
- ✅ Проверка кода на соответствие PEP 8
- ✅ Поиск потенциальных багов и проблем
- ✅ Советы по рефакторингу и улучшению кода
- ✅ Рекомендации по производительности

**Ограничения:**
- ❌ Работает только с Python (не другие языки)
- ❌ Не пишет код за вас (только примеры и советы)
- ❌ Не делает полный редизайн архитектуры без запроса

### Особенности

- **Ролевая модель** - бот имеет четкую специализацию (Python Code Reviewer)
- **Прозрачность** - команда `/role` показывает возможности и ограничения
- **Персонализация** - команда `/start` приветствует по имени, `/me` показывает профиль
- **User Management** - автоматическое сохранение и обновление данных пользователей
- **PostgreSQL** - история диалогов и профили пользователей сохраняются в БД
- **Persistence** - история и данные пользователей сохраняются при перезапуске бота
- **Soft Delete** - команда `/reset` не удаляет данные, а помечает их как удаленные
- **Изоляция** - каждый пользователь имеет свою историю (даже в групповых чатах)
- **Error Handling** - обработка ошибок API с понятными сообщениями пользователю
- **Timeout защита** - по умолчанию 60 секунд

## 📚 Документация

### 🗺️ Roadmaps

- **[Backend Roadmap](docs/roadmap.md)** - история развития backend (S01-S03 завершены) ✅
- **[Frontend Roadmap](docs/frontend-roadmap.md)** - план разработки веб-интерфейса (F01-F05) 🆕

### 📖 Гайды для разработчиков

> **[Полный набор гайдов](docs/guides/README.md)** - от онбординга до мастерства

**Рекомендуемый порядок для новичков**:
1. **[Getting Started](docs/guides/01_GETTING_STARTED.md)** - быстрый старт за 10 минут ⚡
2. **[Architecture Overview](docs/guides/02_ARCHITECTURE_OVERVIEW.md)** - понимание архитектуры 🏗️
3. **[Codebase Tour](docs/guides/05_CODEBASE_TOUR.md)** - навигация по коду 🗺️
4. **[Development Workflow](docs/guides/08_DEVELOPMENT_WORKFLOW.md)** - процесс разработки по TDD 🔄

**Остальные гайды**:
- [Data Model](docs/guides/03_DATA_MODEL.md) - структуры данных 📊
- [Integrations](docs/guides/04_INTEGRATIONS.md) - Telegram и OpenRouter API 🔌
- [Configuration & Secrets](docs/guides/06_CONFIGURATION_AND_SECRETS.md) - настройка и безопасность 🔐
- [CI/CD](docs/guides/07_CI_CD.md) - автоматизация проверок качества ✅

### 📁 Дополнительные документы

**Backend:**
- [Идея проекта](docs/idea.md) - концепция и цели
- [Техническое видение](docs/vision.md) - полная техническая документация
- [🎨 Архитектурная визуализация](docs/architecture_visualization.md) - диаграммы и схемы проекта
- [Правила разработки](.cursor/rules/) - соглашения для AI-ассистента
  - [Соглашения по коду](.cursor/rules/conventions.mdc) - стиль и архитектура
  - [QA соглашения](.cursor/rules/qa_conventions.mdc) - тестирование и TDD
  - [Workflow](.cursor/rules/workflow.mdc) - процесс разработки
  - [Workflow TDD](.cursor/rules/workflow_tdd.mdc) - разработка по TDD подходу

**Frontend:**
- [Frontend проект](frontend/README.md) - веб-интерфейс (Dashboard готов) ✅
- [Frontend Vision](frontend/doc/frontend-vision.md) - концепция и архитектура
- [Frontend Roadmap](docs/frontend-roadmap.md) - план разработки (F01-F03 завершены)

## 🔧 Качество кода

### Текущие метрики

- ✅ **Ruff**: 0 ошибок (All checks passed)
- ✅ **Mypy**: Success (strict mode, 100% typed)
- ✅ **Tests**: 78+ тестов (63+ юнит + 15+ интеграционных)
- ✅ **Coverage**: 80%+ (100% для ключевых модулей)

### Принципы

1. **SRP** - каждый класс имеет одну ответственность
2. **Типизация** - все функции полностью типизированы
3. **Тестируемость** - юнит-тесты независимы от окружения
4. **Простота** - KISS без избыточных абстракций
5. **CI/CD** - автоматизированные проверки перед коммитом

## 📝 Workflow разработки

1. Создайте ветку для задачи:
```bash
git checkout -b feature/your-feature
```

2. Разрабатывайте с проверками:
```bash
make format  # Форматирование
make lint    # Проверка кода
make test    # Тесты
```

3. Перед коммитом:
```bash
make ci      # Полная проверка
```

4. Коммит изменений:
```bash
git add .
git commit -m "feat: your feature description"
```

5. Создайте Pull Request

## 🗄️ База данных

### Структура

Проект использует PostgreSQL для хранения данных:

**Таблица `users`** - профили пользователей Telegram:
```sql
CREATE TABLE users (
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
```

**Таблица `messages`** - история сообщений:
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    character_count INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
```

### Индексы

**Таблица users:**
- `PRIMARY KEY (user_id)` - уникальность пользователей
- `idx_users_username` - поиск по username
- `idx_users_created_at` - сортировка по дате регистрации

**Таблица messages:**
- `idx_chat_user` - быстрый поиск истории пользователя
- `idx_deleted` - фильтрация удаленных сообщений
- `idx_messages_user_id` - foreign key index

### Soft Delete

Команда `/reset` не удаляет сообщения физически, а устанавливает `deleted_at`:

```python
# Сообщения остаются в БД, но не показываются в истории
deleted_at IS NULL  # активные сообщения
deleted_at IS NOT NULL  # удаленные сообщения
```

### Миграции

Миграции применяются автоматически при запуске бота. Для ручного применения:

```bash
make migrate
```

### Просмотр данных

```bash
# Подключиться к БД
docker exec -it systech-aidd-postgres-1 psql -U postgres -d systech_aidd

# Посмотреть пользователей
SELECT user_id, username, first_name, is_premium, created_at 
FROM users 
ORDER BY created_at DESC;

# Посмотреть сообщения с информацией о пользователе
SELECT m.id, u.first_name, m.role, LEFT(m.content, 50) as content, m.created_at 
FROM messages m
JOIN users u ON m.user_id = u.user_id
WHERE m.deleted_at IS NULL 
ORDER BY m.created_at DESC;

# Статистика пользователя
SELECT u.first_name, COUNT(m.id) as message_count, SUM(m.character_count) as total_chars
FROM users u
LEFT JOIN messages m ON u.user_id = m.user_id AND m.deleted_at IS NULL AND m.role = 'user'
GROUP BY u.user_id, u.first_name;
```

## 🐛 Отладка

### Логи

Логи выводятся в stdout с уровнем INFO:

```
2025-10-11 12:29:36 - __main__ - INFO - Configuration loaded successfully
2025-10-11 12:29:36 - src.bot - INFO - Telegram bot initialized
2025-10-11 12:29:36 - aiogram.dispatcher - INFO - Start polling
```

### Типичные проблемы

**Ошибка импорта модулей:**
- Запускайте через `make run` или `uv run python -m src.main`
- НЕ запускайте напрямую: `python src/main.py`

**Тесты не проходят:**
- Юнит-тесты НЕ требуют .env файл
- Интеграционные тесты требуют валидные API ключи в .env

**Mypy ошибки:**
- Все модули используют строгую типизацию
- Используйте относительные импорты: `from .config import Config`

**PostgreSQL не запускается:**
```bash
# Проверьте статус контейнера
docker compose ps

# Перезапустите БД
docker compose down
docker compose up -d postgres

# Проверьте логи
docker compose logs postgres
```

**Ошибки миграций:**
```bash
# Проверьте подключение к БД
docker exec systech-aidd-postgres-1 psql -U postgres -d systech_aidd -c "SELECT 1;"

# Примените миграции вручную
make migrate
```

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 🤝 Контрибьюция

Контрибьюции приветствуются! Пожалуйста:

1. Следуйте существующему стилю кода
2. Добавляйте тесты для новой функциональности
3. Обновляйте документацию
4. Запускайте `make ci` перед PR

## 📬 Контакты

- Вопросы и предложения: [Issues](https://github.com/yourusername/systech-aidd/issues)
- Документация: [docs/](docs/)

---

**Сделано с ❤️ следуя принципам KISS и ООП**
