# Guides - Руководства по проекту

Полный набор гайдов для онбординга и понимания проекта systech-aidd.

## 🎯 Рекомендуемый порядок чтения

### Для новых разработчиков

1. **[Getting Started](01_GETTING_STARTED.md)** - быстрый старт (10 минут)
2. **[Architecture Overview](02_ARCHITECTURE_OVERVIEW.md)** - общая картина архитектуры
3. **[Codebase Tour](05_CODEBASE_TOUR.md)** - детальная навигация по коду
4. **[Development Workflow](08_DEVELOPMENT_WORKFLOW.md)** - процесс разработки

### Для понимания деталей

5. **[Data Model](03_DATA_MODEL.md)** - структуры данных
6. **[Integrations](04_INTEGRATIONS.md)** - работа с внешними API
7. **[Configuration & Secrets](06_CONFIGURATION_AND_SECRETS.md)** - настройка
8. **[CI/CD](07_CI_CD.md)** - автоматизация проверок

---

## 📚 Содержание гайдов

### [01. Getting Started](01_GETTING_STARTED.md)

**Для кого**: Абсолютные новички в проекте

**Что внутри**:
- Предварительные требования (Python, uv, git)
- Установка зависимостей
- Настройка `.env` (получение API ключей)
- Первый запуск бота
- Запуск тестов
- Типичные проблемы

**Время**: ~10 минут

---

### [02. Architecture Overview](02_ARCHITECTURE_OVERVIEW.md)

**Для кого**: Разработчики, изучающие архитектуру

**Что внутри**:
- Принципы проекта (KISS, ООП, SRP, TDD)
- Архитектурная схема с диаграммами
- Поток данных (User → Telegram → Handler → LLM → Response)
- Компоненты системы (main, config, bot, handlers, llm_client, conversation)
- Ролевая модель AI-продукта
- Технологический стек с обоснованием
- Взаимодействие компонентов
- Обработка ошибок

**Диаграммы**: Mermaid (архитектура, sequence, tech stack, error handling)

---

### [03. Data Model](03_DATA_MODEL.md)

**Для кого**: Разработчики, работающие с данными

**Что внутри**:
- Config - структура конфигурации (Pydantic)
- Message - формат сообщения (role, content, timestamp)
- Conversation Storage - хранилище диалогов (defaultdict, in-memory)
- Системный промпт (SYSTEM_PROMPT)
- Операции с данными (add, get, clear)
- Жизненный цикл сообщений
- Ограничение истории
- Особенности in-memory storage

**Диаграммы**: Mermaid (data flow, storage structure)

---

### [04. Integrations](04_INTEGRATIONS.md)

**Для кого**: Разработчики, работающие с API

**Что внутри**:
- **Telegram Bot API**: aiogram 3.x, polling, обработка сообщений
- **OpenRouter API**: openai SDK, формат запросов/ответов
- Обработка ошибок (APITimeoutError, APIError, LLMError)
- Rate limits и ограничения
- Мокирование в тестах
- Безопасность (API ключи, HTTPS, timeout)

**Диаграммы**: Mermaid (integrations overview, polling, request flow)

---

### [05. Codebase Tour](05_CODEBASE_TOUR.md)

**Для кого**: Разработчики, изучающие код

**Что внутри**:
- Полная структура проекта (дерево файлов)
- **src/** - детальное описание каждого модуля:
  - `main.py` - точка входа, инициализация
  - `config.py` - Pydantic конфигурация
  - `bot.py` - Telegram Bot, регистрация handlers
  - `handlers.py` - обработка команд и сообщений
  - `llm_client.py` - LLM клиент, исключения
  - `conversation.py` - хранилище диалогов
- **tests/** - организация тестов (юнит vs интеграционные)
- Конфигурационные файлы (Makefile, pyproject.toml, pytest.ini)
- `.cursor/rules/` - правила для AI-ассистента
- Навигация по коду (где искать что)
- Метрики проекта (coverage, tests, LOC)

**Диаграммы**: Mermaid (module dependencies, handler flow)

---

### [06. Configuration and Secrets](06_CONFIGURATION_AND_SECRETS.md)

**Для кого**: Разработчики, настраивающие окружение

**Что внутри**:
- Структура `.env` файла (все параметры)
- **Получение API ключей**:
  - Telegram Bot Token (@BotFather)
  - OpenRouter API Key (openrouter.ai)
- Выбор модели LLM
- Системный промпт (структура, примеры ролей)
- Pydantic валидация (типы, обязательные поля)
- Безопасность (что НЕ коммитить, логирование)
- Разные окружения (dev, prod)
- Отладка проблем конфигурации
- Параметры LLM (TEMPERATURE, MAX_TOKENS, TIMEOUT)

**Диаграммы**: Mermaid (config flow, token acquisition, validation)

---

### [07. CI/CD](07_CI_CD.md)

**Для кого**: Разработчики, работающие с качеством кода

**Что внутри**:
- Makefile - все команды автоматизации
- **Инструменты качества**:
  - **Ruff** - линтер и форматтер (конфигурация, правила)
  - **Mypy** - статическая проверка типов (strict mode)
  - **Pytest** - тестирование (маркеры, команды)
  - **Pytest-cov** - coverage (отчеты, метрики)
- `make ci` - комплексная проверка
- Workflow разработки (format → lint → test → ci → commit)
- Текущие метрики качества (81% coverage, 0 errors)
- Решение распространенных проблем

**Диаграммы**: Mermaid (CI/CD flow, workflow)

---

### [08. Development Workflow](08_DEVELOPMENT_WORKFLOW.md)

**Для кого**: Все разработчики

**Что внутри**:
- Принципы разработки (TDD, KISS, SRP)
- **Этапы разработки**:
  1. Анализ задачи
  2. Планирование решения (тест-кейсы)
  3. Согласование
  4. Реализация по TDD (🔴 RED → 🟢 GREEN → 🔵 REFACTOR)
  5. Проверка качества (`make ci`)
  6. Коммит изменений
- Типы тестов (юнит vs интеграционные)
- Code Review процесс (чеклист PR, критерии)
- Работа с таск-листом (`docs/tasklist.md`)
- Быстрая справка команд
- Соглашения по коду (именование, типизация, docstrings)
- Распространенные паттерны (обработка ошибок, моки)

**Диаграммы**: Mermaid (TDD cycle, full workflow)

---

## 🔍 Быстрая навигация по темам

### Начало работы
- Установка → [01. Getting Started](01_GETTING_STARTED.md)
- Настройка `.env` → [06. Configuration & Secrets](06_CONFIGURATION_AND_SECRETS.md)
- Первый запуск → [01. Getting Started](01_GETTING_STARTED.md)

### Понимание кода
- Архитектура → [02. Architecture Overview](02_ARCHITECTURE_OVERVIEW.md)
- Где что находится → [05. Codebase Tour](05_CODEBASE_TOUR.md)
- Как работают данные → [03. Data Model](03_DATA_MODEL.md)

### Разработка
- Процесс разработки → [08. Development Workflow](08_DEVELOPMENT_WORKFLOW.md)
- TDD подход → [08. Development Workflow](08_DEVELOPMENT_WORKFLOW.md#4-реализация-по-tdd)
- Тестирование → [07. CI/CD](07_CI_CD.md#3-pytest---тестирование)

### API и интеграции
- Telegram API → [04. Integrations](04_INTEGRATIONS.md#telegram-bot-api)
- OpenRouter API → [04. Integrations](04_INTEGRATIONS.md#openrouter-api)
- Обработка ошибок → [04. Integrations](04_INTEGRATIONS.md#обработка-ошибок)

### Качество кода
- Линтинг и форматирование → [07. CI/CD](07_CI_CD.md#1-ruff---линтер-и-форматтер)
- Типизация → [07. CI/CD](07_CI_CD.md#2-mypy---статическая-проверка-типов)
- Coverage → [07. CI/CD](07_CI_CD.md#4-pytest-cov---coverage)

---

## 📖 Дополнительная документация

### В корне docs/
- **[idea.md](../idea.md)** - концепция ролевого AI-продукта
- **[vision.md](../vision.md)** - полное техническое видение
- **[tasklist.md](../tasklist.md)** - основные задачи разработки
- **[tasklist_tech_dept.md](../tasklist_tech_dept.md)** - технический долг

### В .cursor/rules/
- **[conventions.mdc](../../.cursor/rules/conventions.mdc)** - соглашения по коду
- **[qa_conventions.mdc](../../.cursor/rules/qa_conventions.mdc)** - QA соглашения и TDD
- **[workflow_tdd.mdc](../../.cursor/rules/workflow_tdd.mdc)** - детальный TDD workflow
- **[workflow.mdc](../../.cursor/rules/workflow.mdc)** - базовый процесс разработки

### В корне проекта
- **[README.md](../../README.md)** - основной README проекта

---

## 🎓 Сценарии использования

### Я новый разработчик в проекте
1. [Getting Started](01_GETTING_STARTED.md) - настройте окружение
2. [Architecture Overview](02_ARCHITECTURE_OVERVIEW.md) - поймите архитектуру
3. [Codebase Tour](05_CODEBASE_TOUR.md) - изучите код
4. [Development Workflow](08_DEVELOPMENT_WORKFLOW.md) - начните разрабатывать

### Мне нужно добавить новую функцию
1. [Development Workflow](08_DEVELOPMENT_WORKFLOW.md) - процесс разработки
2. [Codebase Tour](05_CODEBASE_TOUR.md) - найдите где добавлять код
3. [CI/CD](07_CI_CD.md) - проверьте качество

### У меня проблема с API
1. [Integrations](04_INTEGRATIONS.md) - как работают API
2. [Configuration & Secrets](06_CONFIGURATION_AND_SECRETS.md) - проверьте настройки

### Мне нужно изменить модель данных
1. [Data Model](03_DATA_MODEL.md) - текущая модель
2. [Architecture Overview](02_ARCHITECTURE_OVERVIEW.md) - как все связано

### Я хочу улучшить процесс разработки
1. [Development Workflow](08_DEVELOPMENT_WORKFLOW.md) - текущий процесс
2. [CI/CD](07_CI_CD.md) - инструменты автоматизации

---

## 💡 Принципы проекта

Все гайды следуют ключевым принципам:

- **KISS** - максимальная простота
- **ООП** - объектно-ориентированный подход
- **TDD** - разработка через тестирование
- **SRP** - одна ответственность на компонент
- **Типизация** - строгая типизация (mypy strict)
- **Асинхронность** - async/await для I/O

---

## 📊 Статистика проекта

- **Строк кода**: ~491 (src/)
- **Строк тестов**: ~1200+ (tests/)
- **Coverage**: 81%
- **Тестов**: 60 (47 юнит + 13 интеграционных)
- **Ruff errors**: 0
- **Mypy status**: Success (strict)
- **Файлов кода**: 6 (main, config, bot, handlers, llm_client, conversation)

---

## 🤝 Вклад в документацию

Если вы нашли ошибку или хотите улучшить гайды:

1. Создайте issue с описанием проблемы
2. Или создайте PR с исправлениями
3. Следуйте принципам: простота, понятность, краткость

---

**Сделано с ❤️ для команды systech-aidd**

