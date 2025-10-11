# Техническое видение проекта

## 1. Технологии

### Основные технологии
- **Python 3.11+** - основной язык разработки
- **uv** - управление зависимостями и виртуальным окружением
- **aiogram 3.x** - асинхронный фреймворк для Telegram Bot API (polling режим)
- **openai** - клиент для работы с LLM через OpenRouter
- **make** - автоматизация задач сборки и запуска

### Дополнительные библиотеки
- **pydantic** - валидация конфигурации и данных
- **python-dotenv** - управление переменными окружения
- **aiohttp** - асинхронные HTTP-запросы (зависимость aiogram)

### Инструменты разработки
- **ruff** - линтер и форматтер кода (расширенные правила: E, F, I, N, W, B, C4, UP, SIM, RET, ARG)
- **mypy** - статическая проверка типов (strict mode)
- **pytest** - фреймворк для тестирования
- **pytest-asyncio** - поддержка async тестов
- **pytest-cov** - измерение покрытия кода

## 2. Принципы разработки

### Основные принципы
1. **KISS (Keep It Simple, Stupid)** - максимальная простота решений
2. **ООП** - объектно-ориентированный подход с четкой структурой
3. **1 класс = 1 файл** - каждый класс в отдельном файле
4. **Асинхронность** - async/await для работы с Telegram и LLM API
5. **Конфигурация через переменные окружения** - .env файл для настроек
6. **Минимум абстракций** - только необходимые уровни абстракции
7. **Явное лучше неявного** - понятный и читаемый код

### Что НЕ делаем (антипаттерны для MVP)
- ❌ Сложные паттерны проектирования (фабрики, стратегии и т.д.)
- ❌ Избыточная модульность
- ❌ Преждевременная оптимизация
- ❌ Множественные уровни абстракции
- ❌ Базы данных (пока не нужны)

### Подход к реализации
- Прямолинейный код
- Минимальная вложенность классов
- Понятные имена классов и методов
- Каждый компонент делает одну вещь хорошо

## 3. Структура проекта

```
systech-aidd/
├── .env.example          # Пример конфигурации
├── .env                  # Реальная конфигурация (в .gitignore)
├── .gitignore
├── README.md
├── Makefile              # Команды для запуска и управления
├── pyproject.toml        # Конфигурация проекта для uv + mypy + ruff
├── pytest.ini            # Конфигурация pytest и маркеры тестов
├── uv.lock               # Lockfile зависимостей
├── .cursor/
│   └── rules/            # Правила для AI-ассистента
│       ├── conventions.mdc
│       ├── workflow.mdc
│       └── workflow_tech_debt.mdc
├── docs/
│   ├── idea.md
│   ├── vision.md
│   ├── tasklist.md
│   └── tasklist_tech_dept.md
├── src/
│   ├── __init__.py
│   ├── main.py           # Точка входа приложения
│   ├── config.py         # Класс Config - конфигурация из .env
│   ├── bot.py            # Класс TelegramBot - инициализация бота
│   ├── handlers.py       # Класс MessageHandler - обработка сообщений
│   ├── llm_client.py     # Класс LLMClient + LLMError - работа с OpenRouter
│   └── conversation.py   # Класс Conversation - контекст диалога (defaultdict)
└── tests/
    ├── __init__.py
    ├── test_config.py
    ├── test_handlers.py
    ├── test_llm_client.py
    └── test_conversation.py
```

### Описание компонентов

**Основные модули:**
1. **main.py** - запуск приложения, инициализация и старт polling (запускается как модуль: `python -m src.main`)
2. **config.py** - загрузка и валидация конфигурации через Pydantic BaseSettings (токены, API ключи)
3. **bot.py** - инициализация Telegram бота и регистрация handlers
4. **handlers.py** - обработчики Telegram сообщений (/start, /reset, текстовые сообщения) + обработка исключений LLM
5. **llm_client.py** - взаимодействие с LLM через OpenRouter + класс исключения LLMError
6. **conversation.py** - управление историей диалога пользователя (в памяти через defaultdict)

**Тестирование:**
- Юнит-тесты для каждого основного компонента (не зависят от .env)
- Интеграционные тесты помечены маркером `@pytest.mark.integration`
- Использование pytest с async поддержкой (pytest-asyncio)
- Моки для внешних API (Telegram, OpenRouter) в юнит-тестах
- Измерение покрытия кода через pytest-cov (цель: 45%+)

**Всего 6 файлов кода + тесты + строгая типизация** - минимально и достаточно для MVP с высоким качеством кода.

## 4. Архитектура проекта

### Архитектурная схема

```
┌─────────────────────────────────────────┐
│           main.py (Entry Point)         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         config.py (Config)              │ ◄── .env
└─────────────────────────────────────────┘

         ┌───────┴───────┐
         ▼               ▼
┌──────────────┐  ┌──────────────┐
│  bot.py      │  │ llm_client.py│
│(TelegramBot) │  │  (LLMClient) │
└──────┬───────┘  └──────┬───────┘
       │                 │
       ▼                 │
┌──────────────┐         │
│ handlers.py  │         │
│(MessageHandler)◄───────┘
└──────┬───────┘
       │
       ▼
┌──────────────┐
│conversation.py│
│(Conversation)│
└──────────────┘
```

### Поток данных

1. **main.py** → Загружает Config → Создает TelegramBot и LLMClient → Запускает polling
2. **TelegramBot** → Регистрирует MessageHandler
3. **User Message** → MessageHandler → Conversation (добавляет в историю) → LLMClient (запрос к LLM) → Response → User
4. **Conversation** → Хранит историю сообщений в памяти (словарь: "chat_id:user_id" → список сообщений)

### Принципы взаимодействия

- **Config** - независимый, используется всеми
- **TelegramBot** - зависит только от Config
- **LLMClient** - зависит только от Config, бросает исключения (не возвращает UI-сообщения)
- **MessageHandler** - зависит от LLMClient и Conversation, обрабатывает все исключения LLM
- **Conversation** - независимый, использует defaultdict для автоматического создания списков
- **Относительные импорты** - все модули используют относительные импорты (from .config import Config)

### Особенности

- Нет БД - всё в памяти (при перезапуске история теряется)
- Нет сложных зависимостей между компонентами
- Каждый класс имеет четкую ответственность
- Асинхронная обработка через async/await

## 5. Модель данных

### Config (Pydantic BaseSettings)

```python
telegram_bot_token: str           # Токен Telegram бота
openrouter_api_key: str           # API ключ OpenRouter
openrouter_model: str             # Модель LLM (например, "anthropic/claude-3.5-sonnet")
system_prompt: str                # Системный промпт (роль ассистента)
max_history_length: int = 10     # Максимум сообщений в истории
temperature: float = 0.7          # Температура для LLM (креативность)
max_tokens: int = 1000            # Максимум токенов в ответе
timeout: int = 60                 # Таймаут запросов к API (секунды)
```

### Message (простой dict)

```python
{
    "role": str,        # "user" | "assistant" | "system"
    "content": str,     # Текст сообщения
    "timestamp": float  # Unix timestamp (time.time())
}
```

### Conversation Storage (in-memory)

```python
from collections import defaultdict

conversations: defaultdict[str, list[dict]] = defaultdict(list)
# Ключ: "chat_id:user_id" (составной ключ)
# Значение: список сообщений (история диалога)
# defaultdict автоматически создает пустой список для новых пользователей
```

### Пример структуры данных

```python
{
    "123456789:987654321": [  # "chat_id:user_id"
        {"role": "system", "content": "Ты помощник...", "timestamp": 1699000000.0},
        {"role": "user", "content": "Привет!", "timestamp": 1699000001.0},
        {"role": "assistant", "content": "Здравствуйте!", "timestamp": 1699000002.5},
        {"role": "user", "content": "Как дела?", "timestamp": 1699000010.0},
        {"role": "assistant", "content": "Отлично!", "timestamp": 1699000012.3}
    ]
}
```

### Особенности

- **Никаких БД** - вся история в RAM
- **Простые структуры** - dict и list
- **Pydantic** только для Config (валидация при запуске)
- **Составной ключ** - "chat_id:user_id" для разделения истории пользователей в групповых чатах
- **Timestamp** - для каждого сообщения (может пригодиться для отладки и логирования)
- **История ограничена** - храним только последние N сообщений для экономии токенов
- **System prompt** один на всех пользователей (задается в .env)
- **Настраиваемые параметры LLM** - temperature, max_tokens, timeout в конфиге
- **При перезапуске история теряется** - это нормально для MVP

## 6. Работа с LLM

### LLMClient - основной класс

**Исключения:**
```python
class LLMError(Exception):
    """Базовое исключение для ошибок LLM."""
```

**Основной метод:**
```python
async def get_response(
    self, 
    messages: list[dict[str, str]], 
    system_prompt: str | None = None
) -> str
```

**Raises:**
- `Timeout` - если запрос превысил таймаут
- `APIError` - если произошла ошибка OpenRouter API
- `LLMError` - другие ошибки (пустой ответ, неожиданные исключения)

### Реализация

1. **Использование OpenAI SDK** с базовым URL OpenRouter:
   ```python
   base_url = "https://openrouter.ai/api/v1"
   ```

2. **Формат запроса:**
   - Принимает список сообщений в формате OpenAI (только role и content, без timestamp)
   - Отправляет в OpenRouter с параметрами из конфига
   - Возвращает текст ответа ассистента

3. **Параметры запроса:**
   - `model` - из конфига
   - `messages` - история диалога (role + content)
   - `temperature` - из конфига
   - `max_tokens` - из конфига
   - `timeout` - из конфига

4. **Обработка ошибок (Single Responsibility Principle):**
   - **LLMClient** бросает исключения: `Timeout`, `APIError`, `LLMError`
   - **MessageHandler** перехватывает исключения и отправляет UI-сообщения пользователю:
     - `Timeout` → "⏱️ Превышено время ожидания ответа"
     - `APIError` → "❌ Ошибка API: {детали}"
     - `LLMError` → "❌ Ошибка LLM: {детали}"
   - Все ошибки логируются на уровне ERROR с полным трейсбеком

### Особенности

- **Простой интерфейс** - один метод для всего
- **Разделение ответственности** - LLMClient не знает о UI, только бросает исключения
- **Строгая типизация** - все параметры и возвращаемые значения типизированы
- **Без retry** - пока не усложняем (можно добавить потом)
- **Без streaming** - получаем полный ответ сразу
- **Без кеширования** - каждый запрос новый
- **Асинхронность** - await для API запроса
- **Фильтрация timestamp** - перед отправкой в LLM удаляем timestamp из messages

### Пример использования

```python
from openai import APIError, Timeout
from .llm_client import LLMClient, LLMError

llm_client = LLMClient(config)
messages = [{"role": "user", "content": "Привет!"}]

try:
    response = await llm_client.get_response(
        messages=messages,
        system_prompt="Ты помощник..."
    )
except Timeout:
    # Обрабатываем таймаут
    logger.error("LLM timeout")
except APIError as e:
    # Обрабатываем ошибку API
    logger.error(f"API error: {e}")
except LLMError as e:
    # Обрабатываем другие ошибки LLM
    logger.error(f"LLM error: {e}")
```

## 7. Сценарии работы

### Сценарий 1: Первое обращение к боту

1. Пользователь отправляет `/start`
2. Бот отвечает приветственным сообщением с описанием возможностей
3. Создается новая история диалога с system prompt

### Сценарий 2: Обычный диалог

1. Пользователь отправляет текстовое сообщение
2. MessageHandler:
   - Получает chat_id и user_id
   - Формирует ключ "chat_id:user_id"
   - Добавляет сообщение пользователя в историю с timestamp
   - Получает полную историю (включая system prompt)
   - Передает историю (без timestamp) в LLMClient
3. LLMClient отправляет запрос в OpenRouter
4. Получает ответ от LLM
5. MessageHandler:
   - Добавляет ответ ассистента в историю с timestamp
   - Отправляет ответ пользователю в Telegram

### Сценарий 3: Ограничение истории

1. Если история превышает max_history_length:
   - Сохраняем system prompt (первое сообщение)
   - Удаляем самые старые сообщения пользователя и ассистента
   - Оставляем последние N сообщений

### Сценарий 4: Сброс истории диалога

1. Пользователь отправляет `/reset`
2. Бот удаляет всю историю для ключа "chat_id:user_id"
3. Бот отвечает: "История диалога сброшена"
4. При следующем сообщении создается новая история с system prompt

### Сценарий 5: Работа в групповом чате

1. Несколько пользователей пишут в одном чате
2. Каждый пользователь имеет свою историю (благодаря ключу "chat_id:user_id")
3. Истории не пересекаются

### Сценарий 6: Обработка ошибок

1. LLMClient бросает исключение (Timeout, APIError, или LLMError)
2. MessageHandler перехватывает исключение
3. Логирует ошибку с полным трейсбеком на уровне ERROR
4. Отправляет понятное сообщение об ошибке пользователю
5. История сообщений сохраняется, пользователь может повторить запрос
6. При критических ошибках пользователю предлагается использовать /reset

### Доступные команды

- `/start` - запуск бота и приветствие
- `/reset` - сброс истории диалога

## 8. Подход к конфигурированию

### Конфигурация через .env

**Файл `.env` (не коммитится в git):**
```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenRouter API
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# LLM Parameters
TEMPERATURE=0.7
MAX_TOKENS=1000
TIMEOUT=60

# Bot Settings
SYSTEM_PROMPT=Ты полезный AI-ассистент. Отвечай кратко и по существу.
MAX_HISTORY_LENGTH=10
```

**Файл `.env.example` (коммитится в git):**
```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=

# OpenRouter API
OPENROUTER_API_KEY=
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# LLM Parameters
TEMPERATURE=0.7
MAX_TOKENS=1000
TIMEOUT=60

# Bot Settings
SYSTEM_PROMPT=Ты полезный AI-ассистент. Отвечай кратко и по существу.
MAX_HISTORY_LENGTH=10
```

### Класс Config

- Использует **Pydantic BaseSettings** с **SettingsConfigDict**
- Автоматически загружает переменные из `.env`
- Валидирует типы данных при запуске
- Падает с понятной ошибкой, если обязательные параметры не заданы
- Полностью типизирован для mypy strict mode

### Особенности

- **Простота** - один файл .env со всеми настройками
- **Безопасность** - секреты не попадают в git (.env в .gitignore)
- **Валидация** - Pydantic проверяет типы и обязательные поля
- **Пример для пользователя** - .env.example показывает, что нужно заполнить
- **Никаких дополнительных файлов конфигурации** - только .env

## 9. Подход к логгированию

### Настройка логгирования

**Конфигурация:**
- Использовать стандартный модуль `logging` из Python
- Вывод в `stdout` (консоль)
- Формат: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Уровень: `INFO` для production

### Что логируем

**INFO уровень:**
- Запуск бота
- Получение сообщения от пользователя (chat_id, user_id, текст обрезанный до 50 символов)
- Отправка ответа пользователю
- Вызов команд (/start, /reset)
- Успешные запросы к LLM (количество токенов)

**ERROR уровень:**
- Ошибки при обращении к LLM API
- Ошибки Telegram API
- Timeout ошибки
- Неожиданные исключения

### Что НЕ логируем

- ❌ Полные тексты сообщений (приватность)
- ❌ API ключи и токены
- ❌ DEBUG информацию (пока не нужна для MVP)
- ❌ Трейсбеки в INFO (только в ERROR)

### Особенности

- **Простота** - только стандартный logging, без дополнительных библиотек
- **Никаких файлов** - только stdout (контейнеры потом подхватят)
- **Минимум информации** - только важное
- **Приватность** - не логируем полные сообщения пользователей
- **Отладка** - достаточно информации для понимания, что происходит

### Пример логов

```
2025-10-11 12:29:36 - __main__ - INFO - Configuration loaded successfully
2025-10-11 12:29:36 - src.conversation - INFO - Conversation storage initialized
2025-10-11 12:29:36 - src.llm_client - INFO - LLM client initialized with model: openai/gpt-oss-20b:free
2025-10-11 12:29:36 - src.bot - INFO - Telegram bot initialized
2025-10-11 12:29:36 - src.handlers - INFO - MessageHandler initialized
2025-10-11 12:29:36 - src.bot - INFO - Handlers registered
2025-10-11 12:29:36 - __main__ - INFO - Starting bot polling...
2025-10-11 12:29:36 - aiogram.dispatcher - INFO - Start polling
2025-10-11 12:29:37 - src.handlers - INFO - Message from user 1716154677 in chat 1716154677, length: 20
2025-10-11 12:29:37 - src.llm_client - INFO - Sending request to LLM: 2 messages, model: openai/gpt-oss-20b:free
2025-10-11 12:29:41 - src.llm_client - INFO - LLM response received, length: 21 chars
2025-10-11 12:29:41 - src.handlers - INFO - Response sent to user 1716154677, length: 21
2025-10-11 12:32:10 - src.handlers - INFO - Command /reset from user 1716154677 in chat 1716154677
2025-10-11 12:35:00 - src.handlers - ERROR - LLM timeout for user 1716154677
```

---

## 10. Команды разработки (Makefile)

### Основные команды

```bash
# Установка зависимостей
make install          # uv sync

# Запуск бота
make run              # uv run python -m src.main

# Проверка кода
make lint             # ruff check + mypy (strict mode)
make format           # ruff format

# Тестирование
make test             # Все тесты + coverage (HTML отчет)
make test-unit        # Только юнит-тесты (не требуют .env)
make test-integration # Только интеграционные тесты

# CI/CD
make ci               # lint + test-unit (для pre-commit проверки)
```

### Качество кода

**Текущие метрики:**
- ✅ **Ruff**: All checks passed (правила: E, F, I, N, W, B, C4, UP, SIM, RET, ARG)
- ✅ **Mypy**: Success (strict mode, 100% typed)
- ✅ **Tests**: 20 юнит-тестов + 13 интеграционных
- ✅ **Coverage**: 46% общий (100% для config.py и conversation.py)

**Цели:**
- Ruff: 0 ошибок
- Mypy: строгая типизация всех модулей
- Coverage: минимум 45%, цель 80%+
- Тесты: все юнит-тесты не зависят от внешних ресурсов

---

## Итого

Данный документ описывает техническое видение для создания простого LLM-ассистента в виде Telegram-бота. Следуя принципам KISS и ООП, с применением современных практик разработки, мы получаем:

- **6 файлов кода** (main, config, bot, handlers, llm_client, conversation)
- **Минимум зависимостей** (aiogram, openai, pydantic, python-dotenv)
- **Простая архитектура** без избыточных абстракций
- **Строгая типизация** (mypy strict mode)
- **Качественные тесты** (юнит + интеграционные)
- **Автоматизация проверок** (make ci)
- **Готовность к запуску** за минимальное время

**Принципы качества кода:**
1. **SRP** - каждый класс имеет одну ответственность (error handling в handlers, не в llm_client)
2. **Типизация** - все функции и методы полностью типизированы
3. **Тестируемость** - юнит-тесты независимы от окружения
4. **Простота** - defaultdict вместо явных проверок
5. **CI/CD готовность** - make ci для быстрой проверки перед коммитом

Этот проект служит основой для быстрой проверки идеи и может быть легко расширен в будущем при необходимости.


