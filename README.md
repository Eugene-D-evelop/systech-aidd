# systech-aidd

LLM-ассистент в виде Telegram-бота через OpenRouter API

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![Coverage](https://img.shields.io/badge/coverage-46%25-yellow.svg)](https://github.com/pytest-dev/pytest-cov)

## 🚀 Быстрый старт

### Предварительные требования

- **Python 3.11+**
- **uv** - менеджер зависимостей ([установка](https://github.com/astral-sh/uv))

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
```

### Запуск бота

```bash
make run
```

Бот запустится в режиме polling и начнет обрабатывать сообщения.

## 📋 Команды разработки

### Основные команды

```bash
# Установка зависимостей
make install          # uv sync

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
├── main.py           # Точка входа (запуск как модуль)
├── config.py         # Pydantic конфигурация из .env
├── bot.py            # Инициализация Telegram бота
├── handlers.py       # Обработчики сообщений + error handling
├── llm_client.py     # Клиент OpenRouter API + исключения
└── conversation.py   # In-memory хранилище диалогов (defaultdict)
```

### Ключевые особенности

- ✅ **Строгая типизация** - mypy strict mode, 100% typed
- ✅ **SRP** - разделение ответственности (error handling в handlers)
- ✅ **Async/await** - для всех I/O операций
- ✅ **Независимые тесты** - юнит-тесты не требуют .env
- ✅ **Относительные импорты** - правильная структура модулей
- ✅ **defaultdict** - автоматическое создание списков для новых пользователей

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
| `handlers.py` | 52% | ⚠️ |
| `llm_client.py` | 35% | ⚠️ |
| `bot.py` | 0% | ⚠️ |
| `main.py` | 0% | ⚠️ |
| **Всего** | **46%** | ✅ |

Цель: **80%+** (требуются дополнительные интеграционные тесты)

## 📦 Технологии

### Основной стек

- **Python 3.11+** - язык разработки
- **uv** - управление зависимостями
- **aiogram 3.x** - Telegram Bot API (async, polling)
- **openai** - SDK для OpenRouter API
- **pydantic** - валидация конфигурации

### Инструменты качества

- **ruff** - линтер и форматтер (правила: E, F, I, N, W, B, C4, UP, SIM, RET, ARG)
- **mypy** - статическая проверка типов (strict mode)
- **pytest** + **pytest-asyncio** - тестирование
- **pytest-cov** - измерение покрытия кода

## 🤖 Использование бота

### Команды

- `/start` - Запуск бота и приветствие
- `/reset` - Сброс истории диалога

### Особенности

- История диалога сохраняется в памяти (до 10 сообщений по умолчанию)
- При перезапуске бота история теряется
- Каждый пользователь имеет свою историю (даже в групповых чатах)
- Обработка ошибок API с понятными сообщениями пользователю
- Timeout защита (по умолчанию 60 секунд)

## 📚 Документация

- [Идея проекта](docs/idea.md) - концепция и цели
- [Техническое видение](docs/vision.md) - полная техническая документация
- [Список задач](docs/tasklist.md) - основная разработка
- [Технический долг](docs/tasklist_tech_dept.md) - рефакторинг (завершен)
- [Правила разработки](.cursor/rules/) - соглашения для AI-ассистента

## 🔧 Качество кода

### Текущие метрики

- ✅ **Ruff**: 0 ошибок (All checks passed)
- ✅ **Mypy**: Success (strict mode, 100% typed)
- ✅ **Tests**: 20 юнит + 13 интеграционных
- ✅ **Coverage**: 46% (100% для core модулей)

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
