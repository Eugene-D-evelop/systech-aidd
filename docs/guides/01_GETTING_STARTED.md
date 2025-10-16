# Getting Started

Быстрый старт для нового разработчика. Цель: от клонирования до работающего бота за 10 минут.

## Предварительные требования

- **Python 3.11+** - [скачать](https://www.python.org/downloads/)
- **uv** - менеджер зависимостей ([установка](https://github.com/astral-sh/uv))
- **Git** - для клонирования репозитория

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd systech-aidd
```

### 2. Установка зависимостей

```bash
make install
```

Команда выполнит `uv sync` и установит все необходимые пакеты в виртуальное окружение.

### 3. Настройка конфигурации

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
# Telegram Bot Token (получить от @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenRouter API Key (получить на openrouter.ai)
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini

# LLM параметры
TEMPERATURE=0.7
MAX_TOKENS=1000
TIMEOUT=60

# Настройки бота
SYSTEM_PROMPT=Ты - Python Code Reviewer. Анализируешь Python код, находишь баги, предлагаешь улучшения. Работаешь только с Python, не пишешь код за пользователя.
MAX_HISTORY_LENGTH=10
```

### 4. Получение API ключей

#### Telegram Bot Token

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям (выберите имя и username)
4. Скопируйте полученный токен в `.env`

#### OpenRouter API Key

1. Зарегистрируйтесь на [openrouter.ai](https://openrouter.ai/)
2. Перейдите в [Keys](https://openrouter.ai/keys)
3. Создайте новый ключ
4. Скопируйте ключ в `.env`

## Запуск

### Запуск бота

```bash
make run
```

Вы должны увидеть логи:

```
2025-10-16 12:00:00 - __main__ - INFO - Configuration loaded successfully
2025-10-16 12:00:00 - src.conversation - INFO - Conversation storage initialized
2025-10-16 12:00:00 - src.llm_client - INFO - LLM client initialized with model: openai/gpt-4o-mini
2025-10-16 12:00:00 - src.bot - INFO - Telegram bot initialized
2025-10-16 12:00:00 - src.handlers - INFO - MessageHandler initialized
2025-10-16 12:00:00 - src.bot - INFO - Handlers registered
2025-10-16 12:00:00 - __main__ - INFO - Starting bot polling...
2025-10-16 12:00:00 - aiogram.dispatcher - INFO - Start polling
```

### Проверка работоспособности

1. Откройте Telegram и найдите вашего бота
2. Отправьте `/start`
3. Отправьте любое текстовое сообщение
4. Бот должен ответить

## Запуск тестов

### Юнит-тесты (не требуют .env)

```bash
make test-unit
```

### Все тесты с coverage

```bash
make test
```

## Проверка качества кода

```bash
# Форматирование
make format

# Линтинг и типизация
make lint

# Комплексная проверка (CI)
make ci
```

## Типичные проблемы

### Ошибка: "Failed to load configuration"

**Причина**: Отсутствует `.env` или не заполнены обязательные поля.

**Решение**: Проверьте наличие `.env` и заполнение всех обязательных параметров.

### Ошибка: ModuleNotFoundError

**Причина**: Неправильный способ запуска.

**Решение**: Используйте `make run` (не `python src/main.py`).

### Тесты не проходят

**Причина**: Для интеграционных тестов нужен `.env`.

**Решение**: Запускайте `make test-unit` для юнит-тестов без зависимостей.

## Что дальше?

- [Обзор архитектуры](02_ARCHITECTURE_OVERVIEW.md) - поймите как все устроено
- [🎨 Архитектурная визуализация](../architecture_visualization.md) - визуальное представление системы
- [Codebase Tour](05_CODEBASE_TOUR.md) - детальная навигация по коду
- [Development Workflow](08_DEVELOPMENT_WORKFLOW.md) - процесс разработки

---

**Готово!** 🎉 Бот работает, можно начинать разработку.

