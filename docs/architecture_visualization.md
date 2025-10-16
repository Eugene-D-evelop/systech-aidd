# 🎨 Архитектурная Визуализация Проекта

> **Комплексное визуальное представление проекта systech-aidd с использованием различных типов диаграмм**

## 📋 Содержание

1. [Контекстная диаграмма (C4 Context)](#1-контекстная-диаграмма-c4-context)
2. [Компонентная архитектура](#2-компонентная-архитектура)
3. [Диаграмма классов](#3-диаграмма-классов)
4. [Диаграмма последовательности](#4-диаграмма-последовательности-sequence)
5. [Диаграмма состояний](#5-диаграмма-состояний-state)
6. [Поток данных (Data Flow)](#6-поток-данных-data-flow)
7. [Жизненный цикл сообщения](#7-жизненный-цикл-сообщения)
8. [Обработка ошибок](#8-обработка-ошибок-error-handling)
9. [User Journey (Путь пользователя)](#9-user-journey-путь-пользователя)
10. [Deployment Architecture](#10-deployment-architecture)
11. [Структура хранения данных](#11-структура-хранения-данных)
12. [CI/CD Pipeline](#12-cicd-pipeline)

---

## 1. Контекстная диаграмма (C4 Context)

**Точка зрения:** Внешний наблюдатель - как система взаимодействует с внешним миром

```mermaid
graph TB
    User[👤 Пользователь<br/>Telegram User]:::userStyle
    Bot[🤖 Systech-AIDD Bot<br/>Python Code Reviewer]:::systemStyle
    TelegramAPI[📱 Telegram API<br/>Bot API]:::externalStyle
    OpenRouter[🧠 OpenRouter API<br/>LLM Gateway]:::externalStyle
    LLM[🎯 LLM Model<br/>GPT/Claude/etc]:::externalStyle

    User -->|"Отправляет код<br/>на ревью"| Bot
    Bot -->|"Возвращает<br/>анализ кода"| User
    Bot <-->|"Polling/Webhooks<br/>aiogram"| TelegramAPI
    Bot <-->|"Chat Completions<br/>OpenAI SDK"| OpenRouter
    OpenRouter <-->|"Маршрутизация<br/>запросов"| LLM

    classDef userStyle fill:#FF6B6B,stroke:#C92A2A,stroke-width:3px,color:#FFF
    classDef systemStyle fill:#4ECDC4,stroke:#0A7C74,stroke-width:4px,color:#FFF
    classDef externalStyle fill:#95E1D3,stroke:#38A98F,stroke-width:2px,color:#000
```

### Описание взаимодействий:
- **Пользователь → Bot**: Отправка Python кода для анализа через Telegram
- **Bot ↔ Telegram API**: Двунаправленное взаимодействие через polling (aiogram)
- **Bot ↔ OpenRouter**: HTTP запросы через OpenAI SDK
- **OpenRouter ↔ LLM**: Маршрутизация к различным LLM провайдерам

---

## 2. Компонентная архитектура

**Точка зрения:** Разработчик - внутренняя структура приложения

```mermaid
graph TB
    subgraph "🎯 Entry Point"
        Main[main.py<br/>Entry Point]:::entryStyle
    end

    subgraph "⚙️ Configuration Layer"
        Config[config.py<br/>Pydantic Settings]:::configStyle
        Env[.env<br/>Environment Variables]:::configStyle
    end

    subgraph "🤖 Telegram Layer"
        Bot[bot.py<br/>TelegramBot]:::telegramStyle
        Handlers[handlers.py<br/>MessageHandler]:::telegramStyle
    end

    subgraph "🧠 Business Logic Layer"
        LLMClient[llm_client.py<br/>LLMClient]:::logicStyle
        Conversation[conversation.py<br/>Conversation]:::logicStyle
    end

    subgraph "🌐 External Services"
        TG_API[Telegram Bot API]:::externalStyle
        OR_API[OpenRouter API]:::externalStyle
    end

    Main --> Config
    Main --> Bot
    Main --> Handlers
    Main --> LLMClient
    Main --> Conversation
    
    Config -.->|load| Env
    Bot --> Config
    Bot --> Handlers
    
    Handlers --> Config
    Handlers --> LLMClient
    Handlers --> Conversation
    
    LLMClient --> Config
    LLMClient --> OR_API
    
    Bot --> TG_API
    Handlers --> TG_API

    classDef entryStyle fill:#FFD93D,stroke:#F4A900,stroke-width:4px,color:#000
    classDef configStyle fill:#6BCB77,stroke:#2F9E44,stroke-width:3px,color:#FFF
    classDef telegramStyle fill:#4D96FF,stroke:#1E5A9E,stroke-width:3px,color:#FFF
    classDef logicStyle fill:#9B59B6,stroke:#6C3483,stroke-width:3px,color:#FFF
    classDef externalStyle fill:#E74C3C,stroke:#C0392B,stroke-width:2px,color:#FFF
```

### Слои приложения:
- **Entry Point**: Точка входа и инициализация
- **Configuration**: Управление конфигурацией через Pydantic
- **Telegram Layer**: Взаимодействие с Telegram Bot API
- **Business Logic**: Обработка диалогов и LLM запросов
- **External Services**: Внешние API

---

## 3. Диаграмма классов

**Точка зрения:** Архитектор - структура объектов и их отношения

```mermaid
classDiagram
    class Config {
        +str telegram_bot_token
        +str openrouter_api_key
        +str openrouter_model
        +str system_prompt
        +int max_history_length
        +float temperature
        +int max_tokens
        +int timeout
    }

    class TelegramBot {
        -Config config
        -Bot bot
        -Dispatcher dp
        +__init__(config: Config)
        +register_handlers(handler: MessageHandler)
        +start() async
    }

    class MessageHandler {
        -Config config
        -LLMClient llm_client
        -Conversation conversation
        +__init__(config, llm_client, conversation)
        +start_command(message: Message) async
        +role_command(message: Message) async
        +reset_command(message: Message) async
        +handle_message(message: Message) async
    }

    class LLMClient {
        -Config config
        -AsyncOpenAI client
        +__init__(config: Config)
        +get_response(messages: list, system_prompt: str) async str
        +test_connection() async bool
    }

    class Conversation {
        -dict~str, list~ conversations
        +add_message(chat_id, user_id, role, content)
        +get_history(chat_id, user_id, limit) list
        +clear_history(chat_id, user_id)
        +get_stats() dict
        -_get_user_key(chat_id, user_id) str
    }

    class LLMError {
        <<exception>>
    }

    TelegramBot --> Config : uses
    TelegramBot --> MessageHandler : registers
    MessageHandler --> Config : uses
    MessageHandler --> LLMClient : uses
    MessageHandler --> Conversation : uses
    LLMClient --> Config : uses
    LLMClient --> LLMError : raises

    style Config fill:#F39C12,stroke:#D68910,stroke-width:3px,color:#FFF
    style TelegramBot fill:#3498DB,stroke:#2874A6,stroke-width:3px,color:#FFF
    style MessageHandler fill:#E74C3C,stroke:#C0392B,stroke-width:3px,color:#FFF
    style LLMClient fill:#9B59B6,stroke:#7D3C98,stroke-width:3px,color:#FFF
    style Conversation fill:#1ABC9C,stroke:#148F77,stroke-width:3px,color:#FFF
    style LLMError fill:#E67E22,stroke:#CA6F1E,stroke-width:2px,color:#FFF
```

### Паттерны проектирования:
- **Single Responsibility**: Каждый класс имеет одну ответственность
- **Dependency Injection**: Config передается в конструкторы
- **Composition over Inheritance**: Композиция объектов вместо наследования

---

## 4. Диаграмма последовательности (Sequence)

**Точка зрения:** Разработчик - как компоненты взаимодействуют во времени

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 User
    participant TG as 📱 Telegram API
    participant Bot as 🤖 Bot
    participant Handler as 🎯 MessageHandler
    participant Conv as 💾 Conversation
    participant LLM as 🧠 LLMClient
    participant OR as 🌐 OpenRouter

    User->>TG: Отправить сообщение с кодом
    TG->>Bot: Update (polling)
    Bot->>Handler: handle_message(message)
    
    rect rgb(255, 230, 200)
        Note over Handler,Conv: Управление контекстом
        Handler->>Conv: add_message(chat_id, user_id, "user", text)
        Handler->>Conv: get_history(chat_id, user_id, limit=10)
        Conv-->>Handler: history: list[dict]
    end
    
    Handler->>TG: send_chat_action("typing")
    
    rect rgb(200, 230, 255)
        Note over Handler,OR: LLM Processing
        Handler->>LLM: get_response(messages, system_prompt)
        LLM->>OR: chat.completions.create(model, messages)
        OR-->>LLM: completion response
        LLM-->>Handler: answer: str
    end
    
    rect rgb(200, 255, 230)
        Note over Handler,User: Ответ пользователю
        Handler->>Conv: add_message(chat_id, user_id, "assistant", answer)
        Handler->>TG: answer(response_text)
        TG->>User: Показать ответ
    end

    Note over User,OR: ✅ Успешный сценарий обработки
```

### Ключевые этапы:
1. **Получение сообщения**: Telegram API → Bot → Handler
2. **Управление контекстом**: Добавление в историю + получение контекста
3. **LLM Processing**: Запрос к OpenRouter и получение ответа
4. **Ответ пользователю**: Сохранение в историю + отправка через Telegram

---

## 5. Диаграмма состояний (State)

**Точка зрения:** Аналитик - жизненный цикл диалога

```mermaid
stateDiagram-v2
    [*] --> NoHistory: Новый пользователь
    
    NoHistory --> Active: /start или первое сообщение
    
    state Active {
        [*] --> WaitingUserMessage
        WaitingUserMessage --> ProcessingLLM: Получено сообщение
        ProcessingLLM --> SendingResponse: LLM ответил
        SendingResponse --> WaitingUserMessage: Ответ отправлен
        
        ProcessingLLM --> ErrorHandling: Timeout/APIError
        ErrorHandling --> WaitingUserMessage: Показ ошибки пользователю
    }
    
    Active --> HistoryFull: history.length >= max_history_length
    HistoryFull --> Active: Удалены старые сообщения
    
    Active --> Reset: /reset команда
    Reset --> NoHistory: История очищена
    
    Active --> ShowingRole: /role команда
    ShowingRole --> Active: Показана роль
    
    NoHistory --> [*]: Бот перезапущен
    Active --> [*]: Бот перезапущен
    HistoryFull --> [*]: Бот перезапущен

    note right of NoHistory
        In-memory storage
        Потеря при рестарте
    end note

    note right of ProcessingLLM
        Таймаут: 60 сек
        Retry: нет
    end note

    note right of HistoryFull
        Лимит: 10 сообщений
        Удаление старых
    end note
```

### Состояния системы:
- **NoHistory**: Новый пользователь без истории
- **Active**: Активный диалог с пользователем
- **ProcessingLLM**: Обработка запроса к LLM
- **ErrorHandling**: Обработка ошибок API
- **HistoryFull**: Превышен лимит истории
- **Reset**: Сброс истории диалога
- **ShowingRole**: Отображение роли бота

---

## 6. Поток данных (Data Flow)

**Точка зрения:** Data Engineer - как данные трансформируются в системе

```mermaid
graph LR
    subgraph "📥 INPUT"
        A[User Message<br/>plain text]:::inputStyle
    end

    subgraph "🔄 TRANSFORMATION"
        B[Message Object<br/>aiogram.types.Message]:::transformStyle
        C[Message Dict<br/>role: user<br/>content: text<br/>timestamp: float]:::transformStyle
        D[History Array<br/>list of messages]:::transformStyle
        E[API Request<br/>OpenAI format<br/>no timestamp]:::transformStyle
    end

    subgraph "🧠 PROCESSING"
        F[LLM Response<br/>raw completion]:::processStyle
        G[Response String<br/>extracted text]:::processStyle
    end

    subgraph "💾 STORAGE"
        H[In-Memory Store<br/>conversations dict]:::storageStyle
        I[User Key<br/>chat_id:user_id]:::storageStyle
    end

    subgraph "📤 OUTPUT"
        J[Telegram Message<br/>HTML formatted]:::outputStyle
    end

    A --> B
    B --> C
    C --> I
    I --> H
    H --> D
    D --> E
    E --> F
    F --> G
    G --> I
    I --> H
    G --> J

    classDef inputStyle fill:#FF6B6B,stroke:#E03131,stroke-width:3px,color:#FFF
    classDef transformStyle fill:#4DABF7,stroke:#1971C2,stroke-width:2px,color:#FFF
    classDef processStyle fill:#9775FA,stroke:#7048E8,stroke-width:3px,color:#FFF
    classDef storageStyle fill:#51CF66,stroke:#2F9E44,stroke-width:2px,color:#FFF
    classDef outputStyle fill:#FFD43B,stroke:#FAB005,stroke-width:3px,color:#000
```

### Трансформации данных:
1. **Input**: Текст от пользователя
2. **Message Object**: aiogram Message с метаданными
3. **Message Dict**: Структура с role/content/timestamp
4. **Storage**: Сохранение в in-memory словарь
5. **History Array**: Список сообщений для контекста
6. **API Request**: Формат OpenAI (без timestamp)
7. **LLM Response**: Ответ от модели
8. **Output**: HTML-форматированное сообщение

---

## 7. Жизненный цикл сообщения

**Точка зрения:** DevOps - путь сообщения через систему

```mermaid
journey
    title Путь пользовательского сообщения через систему
    section Получение
      Пользователь отправляет код: 5: User
      Telegram получает сообщение: 5: Telegram
      Bot polling получает Update: 4: Bot
      Dispatcher маршрутизирует: 4: Bot
    section Обработка
      Handler получает сообщение: 4: Handler
      Извлечение chat_id & user_id: 5: Handler
      Добавление в историю: 5: Conversation
      Получение полной истории: 4: Conversation
    section LLM запрос
      Формирование запроса: 4: LLMClient
      Отправка в OpenRouter: 3: LLMClient
      Ожидание ответа (timeout 60s): 2: OpenRouter
      Парсинг ответа: 4: LLMClient
    section Возврат результата
      Сохранение ответа в историю: 5: Conversation
      Форматирование для Telegram: 5: Handler
      Отправка через Bot API: 4: Telegram
      Пользователь видит ответ: 5: User
```

### Этапы обработки:
- **Получение**: 0-2 сек (зависит от polling interval)
- **Обработка**: < 100 мс (in-memory операции)
- **LLM запрос**: 2-60 сек (зависит от модели и нагрузки)
- **Возврат результата**: < 500 мс

---

## 8. Обработка ошибок (Error Handling)

**Точка зрения:** QA Engineer - потоки обработки ошибок

```mermaid
graph TD
    Start[🚀 Запрос к LLM]:::startStyle
    Request[LLMClient.get_response]:::normalStyle
    
    Success{✅ Успех?}:::decisionStyle
    EmptyCheck{Пустой ответ?}:::decisionStyle
    
    Timeout[⏱️ APITimeoutError]:::errorStyle
    APIErr[❌ APIError]:::errorStyle
    LLMErr[⚠️ LLMError]:::errorStyle
    UnexpErr[💥 Exception]:::errorStyle
    
    HandleTimeout[Handler: Timeout UI message]:::handlerStyle
    HandleAPI[Handler: API Error UI message]:::handlerStyle
    HandleLLM[Handler: LLM Error UI message]:::handlerStyle
    
    LogError[📝 Logger.error with traceback]:::logStyle
    
    UserMsg[📱 Отправка сообщения пользователю]:::outputStyle
    HistorySaved[💾 История сохранена]:::saveStyle
    End[🏁 Готов к новому запросу]:::endStyle

    Start --> Request
    Request --> Success
    
    Success -->|Yes| EmptyCheck
    EmptyCheck -->|No| HistorySaved
    EmptyCheck -->|Yes| LLMErr
    
    Success -->|Timeout| Timeout
    Success -->|API Error| APIErr
    Success -->|Other Error| UnexpErr
    
    Timeout --> LogError
    APIErr --> LogError
    UnexpErr --> LLMErr
    LLMErr --> LogError
    
    LogError --> HandleTimeout
    LogError --> HandleAPI
    Timeout --> HandleTimeout
    APIErr --> HandleAPI
    LLMErr --> HandleLLM
    
    HandleTimeout --> UserMsg
    HandleAPI --> UserMsg
    HandleLLM --> UserMsg
    
    HistorySaved --> UserMsg
    UserMsg --> End

    classDef startStyle fill:#4ECDC4,stroke:#0A7C74,stroke-width:3px,color:#FFF
    classDef normalStyle fill:#95E1D3,stroke:#38A98F,stroke-width:2px,color:#000
    classDef decisionStyle fill:#FFE66D,stroke:#F4A900,stroke-width:3px,color:#000
    classDef errorStyle fill:#FF6B6B,stroke:#C92A2A,stroke-width:3px,color:#FFF
    classDef handlerStyle fill:#A8DADC,stroke:#457B9D,stroke-width:2px,color:#000
    classDef logStyle fill:#F1FAEE,stroke:#1D3557,stroke-width:2px,color:#000
    classDef outputStyle fill:#E63946,stroke:#A4161A,stroke-width:2px,color:#FFF
    classDef saveStyle fill:#06FFA5,stroke:#02C875,stroke-width:2px,color:#000
    classDef endStyle fill:#4ECDC4,stroke:#0A7C74,stroke-width:3px,color:#FFF
```

### Типы ошибок и их обработка:

| Ошибка | Источник | Обработчик | Действие |
|--------|----------|------------|----------|
| `APITimeoutError` | OpenRouter | MessageHandler | "⏱️ Превышено время ожидания (60с)" |
| `APIError` | OpenRouter | MessageHandler | "❌ Ошибка API: {details}" |
| `LLMError` | LLMClient | MessageHandler | "⚠️ Ошибка LLM: {details}" |
| `Exception` | Любой | MessageHandler | "💥 Непредвиденная ошибка" |

---

## 9. User Journey (Путь пользователя)

**Точка зрения:** UX Designer - взаимодействие с ботом

```mermaid
graph TD
    Start([👤 Пользователь открывает бота]):::userStyle
    
    StartCmd[/start - Приветствие]:::cmdStyle
    Welcome["👋 Привет! Я Python Code Reviewer<br/>💡 Команды: /role, /reset"]:::msgStyle
    
    Choice1{Что делать?}:::choiceStyle
    
    RoleCmd[/role - Узнать о роли]:::cmdStyle
    RoleInfo["🎭 Моя роль: Python Code Reviewer<br/>📋 Специализация:<br/>• PEP 8 проверка<br/>• Поиск багов<br/>• Советы по рефакторингу"]:::msgStyle
    
    SendCode[📝 Отправить Python код]:::actionStyle
    Typing[⌨️ Bot typing...]:::processStyle
    Review["✅ Анализ кода:<br/>1. Соответствие PEP 8<br/>2. Потенциальные баги<br/>3. Рекомендации"]:::msgStyle
    
    Continue{Продолжить?}:::choiceStyle
    
    MoreCode[📝 Отправить еще код]:::actionStyle
    ResetCmd[/reset - Новый диалог]:::cmdStyle
    ResetMsg["🔄 История очищена!"]:::msgStyle
    
    Exit([👋 Пользователь закрывает чат]):::endStyle

    Start --> StartCmd
    StartCmd --> Welcome
    Welcome --> Choice1
    
    Choice1 -->|"Узнать больше"| RoleCmd
    RoleCmd --> RoleInfo
    RoleInfo --> Choice1
    
    Choice1 -->|"Отправить код"| SendCode
    SendCode --> Typing
    Typing --> Review
    Review --> Continue
    
    Continue -->|"Да"| MoreCode
    MoreCode --> Typing
    
    Continue -->|"Сбросить"| ResetCmd
    ResetCmd --> ResetMsg
    ResetMsg --> Choice1
    
    Continue -->|"Выход"| Exit

    classDef userStyle fill:#FF6B6B,stroke:#C92A2A,stroke-width:4px,color:#FFF
    classDef cmdStyle fill:#4DABF7,stroke:#1971C2,stroke-width:3px,color:#FFF
    classDef msgStyle fill:#51CF66,stroke:#2F9E44,stroke-width:2px,color:#FFF
    classDef choiceStyle fill:#FFD43B,stroke:#FAB005,stroke-width:3px,color:#000
    classDef actionStyle fill:#9775FA,stroke:#7048E8,stroke-width:2px,color:#FFF
    classDef processStyle fill:#FFA94D,stroke:#FD7E14,stroke-width:2px,color:#FFF
    classDef endStyle fill:#868E96,stroke:#495057,stroke-width:3px,color:#FFF
```

### Основные сценарии:
1. **Онбординг**: `/start` → Приветствие → `/role` → Понимание возможностей
2. **Основной флоу**: Отправка кода → Ожидание → Получение ревью → Повтор
3. **Сброс контекста**: `/reset` → Новый диалог

---

## 10. Deployment Architecture

**Точка зрения:** DevOps - развертывание и инфраструктура

```mermaid
graph TB
    subgraph "🖥️ Local Development"
        Dev[Developer Machine]:::devStyle
        LocalEnv[.env file<br/>Local config]:::configStyle
        UVEnv[uv venv<br/>Python 3.11+]:::envStyle
    end

    subgraph "🔧 Development Tools"
        Make[Makefile<br/>Tasks automation]:::toolStyle
        Ruff[Ruff<br/>Linting & Format]:::toolStyle
        Mypy[Mypy<br/>Type checking]:::toolStyle
        Pytest[Pytest<br/>Testing]:::toolStyle
    end

    subgraph "🐳 Production Environment"
        Container[Docker Container<br/>Optional]:::containerStyle
        ProdEnv[Environment Variables<br/>K8s Secrets/ConfigMap]:::configStyle
        App[Python Application<br/>src/main.py]:::appStyle
    end

    subgraph "☁️ External Services"
        TG[Telegram Bot API<br/>api.telegram.org]:::externalStyle
        OR[OpenRouter API<br/>openrouter.ai]:::externalStyle
    end

    subgraph "📊 Monitoring (Future)"
        Logs[Logging<br/>stdout/stderr]:::monitorStyle
        Metrics[Metrics<br/>Prometheus]:::monitorStyle
        Alerts[Alerts<br/>AlertManager]:::monitorStyle
    end

    Dev --> LocalEnv
    Dev --> UVEnv
    Dev --> Make
    Make --> Ruff
    Make --> Mypy
    Make --> Pytest

    UVEnv --> App
    LocalEnv --> App
    ProdEnv --> App
    Container --> App
    
    App --> TG
    App --> OR
    
    App --> Logs
    Logs -.->|Future| Metrics
    Metrics -.->|Future| Alerts

    classDef devStyle fill:#4ECDC4,stroke:#0A7C74,stroke-width:3px,color:#FFF
    classDef configStyle fill:#FFE66D,stroke:#F4A900,stroke-width:2px,color:#000
    classDef envStyle fill:#95E1D3,stroke:#38A98F,stroke-width:2px,color:#000
    classDef toolStyle fill:#A8DADC,stroke:#457B9D,stroke-width:2px,color:#000
    classDef containerStyle fill:#457B9D,stroke:#1D3557,stroke-width:3px,color:#FFF
    classDef appStyle fill:#E63946,stroke:#A4161A,stroke-width:4px,color:#FFF
    classDef externalStyle fill:#F1FAEE,stroke:#1D3557,stroke-width:2px,color:#000
    classDef monitorStyle fill:#06FFA5,stroke:#02C875,stroke-width:2px,color:#000
```

### Окружения:
- **Local Development**: Разработка на локальной машине с uv
- **Production**: Опционально Docker + Kubernetes
- **External Services**: Telegram и OpenRouter API
- **Monitoring**: Логирование (текущее) + метрики (будущее)

---

## 11. Структура хранения данных

**Точка зрения:** Data Architect - организация данных в памяти

```mermaid
graph TB
    subgraph "💾 In-Memory Storage"
        Storage[defaultdict~str, list~<br/>conversations]:::storageStyle
        
        subgraph "🔑 Keys Structure"
            Key1["'123456:789012'<br/>chat_id:user_id"]:::keyStyle
            Key2["'111111:222222'<br/>chat_id:user_id"]:::keyStyle
            KeyN["'NNNNNN:MMMMMM'<br/>chat_id:user_id"]:::keyStyle
        end
        
        subgraph "📝 Messages Array #1"
            Msg1_1["role: 'user'<br/>content: 'Привет!'<br/>timestamp: 1699000001.0"]:::msgStyle
            Msg1_2["role: 'assistant'<br/>content: 'Здравствуйте!'<br/>timestamp: 1699000002.5"]:::msgStyle
            Msg1_3["role: 'user'<br/>content: 'def foo():...'<br/>timestamp: 1699000010.0"]:::msgStyle
        end
        
        subgraph "📝 Messages Array #2"
            Msg2_1["role: 'user'<br/>content: 'Код...'<br/>timestamp: 1699100001.0"]:::msgStyle
            Msg2_2["role: 'assistant'<br/>content: 'Анализ...'<br/>timestamp: 1699100005.0"]:::msgStyle
        end
    end
    
    subgraph "⚙️ Operations"
        Add[add_message<br/>Добавить сообщение]:::opStyle
        Get[get_history<br/>Получить историю]:::opStyle
        Clear[clear_history<br/>Очистить историю]:::opStyle
        Stats[get_stats<br/>Статистика]:::opStyle
    end
    
    Storage --> Key1
    Storage --> Key2
    Storage --> KeyN
    
    Key1 --> Msg1_1
    Key1 --> Msg1_2
    Key1 --> Msg1_3
    
    Key2 --> Msg2_1
    Key2 --> Msg2_2
    
    Add --> Storage
    Get --> Storage
    Clear --> Storage
    Stats --> Storage

    classDef storageStyle fill:#FF6B6B,stroke:#C92A2A,stroke-width:4px,color:#FFF
    classDef keyStyle fill:#4DABF7,stroke:#1971C2,stroke-width:3px,color:#FFF
    classDef msgStyle fill:#51CF66,stroke:#2F9E44,stroke-width:2px,color:#000
    classDef opStyle fill:#FFD43B,stroke:#FAB005,stroke-width:2px,color:#000
```

### Структура данных:
```python
conversations: defaultdict[str, list[dict[str, Any]]] = {
    "chat_id:user_id": [
        {
            "role": "user",
            "content": "message text",
            "timestamp": 1699000001.0
        },
        ...
    ]
}
```

### Особенности:
- **In-Memory**: Все в RAM, нет персистентности
- **Composite Key**: `chat_id:user_id` для разделения пользователей
- **Timestamp**: Для каждого сообщения (отладка/логирование)
- **Auto-Initialize**: defaultdict автоматически создает пустые списки

---

## 12. CI/CD Pipeline

**Точка зрения:** DevOps - процесс проверки качества кода

```mermaid
graph LR
    subgraph "👨‍💻 Developer Workflow"
        Code[💻 Code Changes]:::devStyle
        Branch[🌿 Feature Branch]:::devStyle
    end
    
    subgraph "🧪 Local Checks (make ci)"
        Format[🎨 make format<br/>ruff format]:::checkStyle
        Lint[🔍 make lint<br/>ruff check + mypy]:::checkStyle
        TestUnit[✅ make test-unit<br/>pytest unit tests]:::checkStyle
    end
    
    subgraph "🚀 CI Server (Future)"
        CILint[📋 Lint Check<br/>ruff + mypy]:::ciStyle
        CITest[🧪 Tests<br/>pytest all]:::ciStyle
        CICov[📊 Coverage<br/>pytest-cov 80%+]:::ciStyle
    end
    
    subgraph "✅ Quality Gates"
        RuffOK{Ruff: 0 errors}:::gateStyle
        MypyOK{Mypy: Success}:::gateStyle
        TestOK{Tests: Pass}:::gateStyle
        CovOK{Coverage: 80%+}:::gateStyle
    end
    
    subgraph "📦 Deployment"
        Merge[🔀 Merge to main]:::deployStyle
        Deploy[🚀 Deploy to prod]:::deployStyle
    end

    Code --> Branch
    Branch --> Format
    Format --> Lint
    Lint --> RuffOK
    Lint --> MypyOK
    RuffOK --> TestUnit
    MypyOK --> TestUnit
    TestUnit --> TestOK
    
    TestOK -->|Success| CILint
    CILint --> CITest
    CITest --> CICov
    CICov --> CovOK
    
    CovOK -->|Pass| Merge
    Merge --> Deploy
    
    RuffOK -->|Fail| Code
    MypyOK -->|Fail| Code
    TestOK -->|Fail| Code
    CovOK -->|Fail| Code

    classDef devStyle fill:#4ECDC4,stroke:#0A7C74,stroke-width:3px,color:#FFF
    classDef checkStyle fill:#A8DADC,stroke:#457B9D,stroke-width:2px,color:#000
    classDef ciStyle fill:#457B9D,stroke:#1D3557,stroke-width:2px,color:#FFF
    classDef gateStyle fill:#FFD43B,stroke:#FAB005,stroke-width:3px,color:#000
    classDef deployStyle fill:#06FFA5,stroke:#02C875,stroke-width:3px,color:#000
```

### Этапы проверки:
1. **Local Checks**: `make ci` перед коммитом
   - Ruff format + check (0 errors)
   - Mypy strict mode (100% typed)
   - Unit tests (не требуют .env)

2. **CI Server** (планируется):
   - Все локальные проверки
   - Интеграционные тесты
   - Coverage report (цель: 80%+)

3. **Quality Gates**:
   - Ruff: 0 ошибок ✅
   - Mypy: Success ✅
   - Tests: All pass ✅
   - Coverage: 81% ✅

---

## 📊 Метрики и KPI

### Производительность:
- **Response Time**: 2-10 сек (зависит от LLM)
- **Polling Interval**: По умолчанию aiogram (пуши в реальном времени)
- **Memory Usage**: ~50 MB + история диалогов
- **Timeout**: 60 сек для LLM запросов

### Качество кода:
- **Ruff**: 0 ошибок ✅
- **Mypy**: 100% типизация ✅
- **Test Coverage**: 81% ✅
- **Lines of Code**: ~700 LOC (включая тесты)

### Архитектурные метрики:
- **Modules**: 6 core modules
- **Classes**: 5 main classes
- **Dependencies**: 6 основных библиотек
- **Complexity**: Low (KISS принцип)

---

## 🎯 Выводы

### Архитектурные преимущества:

1. **Простота** (KISS):
   - Минимум абстракций
   - Прямолинейный поток данных
   - Понятные зависимости

2. **Модульность**:
   - Четкое разделение ответственности (SRP)
   - Независимые компоненты
   - Легкая тестируемость

3. **Гибкость**:
   - Ролевая модель через промпты
   - Конфигурация через .env
   - Легко расширяемая архитектура

4. **Качество**:
   - 100% типизация (mypy strict)
   - 81% покрытие тестами
   - Автоматизированные проверки

### Области для улучшения:

1. **Персистентность**: Добавить БД для сохранения истории
2. **Масштабируемость**: Redis для распределенного хранилища
3. **Мониторинг**: Prometheus + Grafana метрики
4. **Deployment**: Docker + Kubernetes
5. **Testing**: Увеличить покрытие до 95%+

---

## 📚 Связанные документы

- [README.md](../README.md) - Основная документация
- [vision.md](./vision.md) - Техническое видение
- [idea.md](./idea.md) - Концепция проекта
- [Guides](./guides/README.md) - Полный набор гайдов для разработчиков
- [conventions.mdc](../.cursor/rules/conventions.mdc) - Соглашения по коду
- [workflow_tdd.mdc](../.cursor/rules/workflow_tdd.mdc) - TDD процесс

---

**Создано:** 2025-10-16  
**Версия:** 1.0  
**Статус:** ✅ Актуально


