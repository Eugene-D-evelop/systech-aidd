<!-- e237053f-91aa-40b7-ac89-161cf0a93ec8 a394d9b9-3cc5-425c-b857-26a8dedb0da3 -->
# План Спринта F04: Реализация ИИ-чата для администратора

## Цель

Создать полноценный веб-интерфейс для AI-чата на основе референса 21st.dev, интегрировать его в дашборд через floating button, и перевести статистику дашборда с Mock API на Real API.

## Контекст

- Референс UI: `frontend/doc/references/21st-ai-chat.md`
- Frontend Vision: `frontend/doc/frontend-vision.md`
- Существующий бот использует: `LLMClient` (OpenRouter), `Conversation` (история в БД), `Database` (PostgreSQL)
- Real API для статистики уже реализован: `src/stats/real_collector.py`
- Текущий dashboard работает с Mock API

## Основные задачи

### 1. Миграция статистики: Mock API → Real API

**Цель:** Перевести дашборд на реальные данные из PostgreSQL

**Файлы:**

- `src/api/app.py` - уже поддерживает переключение через `USE_REAL_STATS`
- `.env` - добавить `USE_REAL_STATS=true`
- `docs/frontend-roadmap.md` - обновить статус Sprint F05

**Задачи:**

- Переключить API на Real StatCollector
- Протестировать работу с реальными данными
- Обновить документацию

### 2. Backend API для чата

**Цель:** Создать REST API endpoint для обработки сообщений чата

**Новые файлы:**

- `src/api/chat.py` - router для chat endpoints
- `src/chat_manager.py` - логика управления веб-чатом

**Изменения:**

- `src/api/app.py` - подключить chat router
- `migrations/003_create_chat_sessions.sql` - таблица для веб-чата

**API спецификация:**

```python
POST /api/chat/message
Request: { 
  "message": str, 
  "session_id": str,
  "mode": "normal" | "admin"  # режим чата
}
Response: { 
  "response": str, 
  "session_id": str,
  "sql_query": str | None  # только для admin режима
}
```

**Реализация:**

- Использовать существующий `LLMClient` для генерации ответов
- Сохранять историю в БД (аналогично telegram боту)
- Поддержка session_id для идентификации пользователя
- Два режима работы:
  - **Normal mode:** Общий AI-ассистент (системный промпт: "Ты AI-ассистент для администратора бота")
  - **Admin mode:** Text2Postgre для вопросов по статистике
- Лимит истории: 10 сообщений (как в telegram боте)

**Text2Postgre Pipeline (Admin режим):**

1. Пользователь задает вопрос на естественном языке
2. LLM генерирует PostgreSQL запрос через специальный промпт
3. Выполнение SQL запроса к БД статистики
4. Результаты передаются обратно в LLM
5. LLM формирует человекочитаемый ответ
6. Ответ + SQL запрос возвращаются клиенту

**Text2Postgre промпт:**

```
Ты эксперт по SQL. Переведи вопрос пользователя в SQL запрос.
База данных PostgreSQL с таблицами:
- users (user_id, username, first_name, language_code, is_premium, created_at)
- messages (id, user_id, chat_id, role, content, character_count, created_at, deleted_at)

Верни ТОЛЬКО SQL запрос, без объяснений.
```

### 3. Frontend: UI компоненты чата

**Цель:** Реализовать компоненты чата на основе референса 21st.dev

**Новые компоненты shadcn/ui:**

- `frontend/src/components/ui/textarea.tsx` - из референса
- `frontend/src/components/ui/scroll-area.tsx` - для скролла сообщений

**Новые компоненты чата:**

- `frontend/src/components/chat/chat-input.tsx` - инпут с кнопкой отправки
- `frontend/src/components/chat/chat-message.tsx` - отображение одного сообщения
- `frontend/src/components/chat/chat-interface.tsx` - основной контейнер чата
- `frontend/src/components/chat/floating-chat-button.tsx` - кнопка в правом нижнем углу
- `frontend/src/components/chat/mode-toggle.tsx` - переключатель режимов (Normal/Admin)

**Структура компонентов:**

```
FloatingChatButton (fixed bottom-right)
  └─ ChatInterface (раскрывающаяся панель)
      ├─ Header (с кнопкой закрыть + ModeToggle)
      ├─ Messages Area (scroll-area)
      │   └─ ChatMessage[] (user/assistant)
      │       └─ SQL badge (только для admin режима)
      └─ ChatInput (textarea + send button)
```

**UI/UX детали:**

- Floating button: иконка MessageCircle (lucide-react), fixed position
- Chat panel: 400px width, 600px height, shadow-lg, rounded-lg
- Animation: smooth open/close transition
- Mobile: full-screen overlay на малых экранах
- Скролл автоматически к последнему сообщению
- Индикатор "typing..." пока ждем ответ

### 4. Frontend: API интеграция и state management

**Цель:** Подключить чат к backend и реализовать сохранение истории

**Новые файлы:**

- `frontend/src/lib/chat-api.ts` - API client для чата
- `frontend/src/types/chat.ts` - TypeScript типы
- `frontend/src/lib/chat-storage.ts` - работа с localStorage

**TypeScript типы:**

```typescript
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatState {
  messages: Message[]
  isOpen: boolean
  isLoading: boolean
  sessionId: string
}
```

**localStorage стратегия:**

- Ключ: `chat-session-id`
- Сохранять: только sessionId (UUID)
- Генерировать session_id при первом открытии (uuid)
- История сообщений хранится ТОЛЬКО в БД, загружается при открытии чата

**API client:**

```typescript
export async function sendMessage(
  message: string,
  sessionId: string
): Promise<string> {
  // POST /api/chat/message
  // return response
}

export async function getChatHistory(
  sessionId: string
): Promise<Message[]> {
  // GET /api/chat/history/{sessionId}
  // return messages from DB
}
```

### 5. Интеграция чата в дашборд

**Цель:** Добавить floating chat button на dashboard page

**Изменения:**

- `frontend/src/app/dashboard/page.tsx` - добавить `<FloatingChatButton />`
- `frontend/src/app/layout.tsx` - или добавить в layout (на всех страницах)

**Решение:** Добавить в `dashboard/page.tsx` (только на dashboard)

### 6. Styling и адаптивность

**Responsive breakpoints:**

- Desktop (≥768px): floating panel 400x600px
- Mobile (<768px): full-screen overlay

**Tailwind classes примеры:**

- Floating button: `fixed bottom-4 right-4 z-50`
- Chat panel: `fixed bottom-20 right-4 w-96 h-[600px] shadow-2xl`
- Mobile: `md:w-96 md:h-[600px] max-md:inset-0 max-md:w-full max-md:h-full`

### 7. Тестирование и полировка

**Чек-лист:**

- ✅ Backend API работает
- ✅ Сообщения сохраняются в БД
- ✅ История загружается из БД
- ✅ UI responsive (desktop + mobile)
- ✅ Loading states работают
- ✅ Error handling
- ✅ Автоскролл к последнему сообщению
- ✅ Real API для статистики работает
- ✅ TypeScript: 0 ошибок
- ✅ ESLint: 0 ошибок
- ✅ Backend тесты: pytest проходят
- ✅ Ruff: 0 ошибок
- ✅ Mypy: 0 ошибок (strict mode)

## Технические детали

### База данных

**Новая миграция `003_create_chat_sessions.sql`:**

```sql
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chat_session ON chat_messages(session_id, created_at);
```

### Dependencies

**Frontend (уже установлены):**

- lucide-react (иконки)
- uuid (для session_id генерации) - нужно установить

**Backend (уже установлены):**

- FastAPI, Pydantic, psycopg

### Архитектурные решения

1. **Session management:** UUID на клиенте, хранится в localStorage
2. **История чата:** localStorage + БД (БД - source of truth)
3. **Real-time:** REST API (не WebSocket) для простоты
4. **Состояние UI:** useState в React (без Redux)
5. **Системный промпт:** Общий AI-ассистент (без Text2SQL в F04)

## Будущие расширения (не в F04)

- Режим администратора с Text2SQL (Sprint F05)
- WebSocket для real-time (опционально)
- Аутентификация пользователей
- Экспорт истории чата
- Voice input (опционально)

## Критерии готовности

- [x] Real API для статистики работает на dashboard
- [x] Backend API для чата готов и протестирован
- [x] UI компоненты чата реализованы
- [x] Floating button интегрирован в dashboard
- [x] История сохраняется в localStorage
- [x] Responsive дизайн работает
- [x] Все TypeScript/ESLint проверки проходят
- [x] Документация обновлена

### To-dos

- [ ] Миграция статистики дашборда с Mock API на Real API
- [ ] Создать backend API endpoints для чата
- [ ] Реализовать ChatManager для управления сессиями
- [ ] Создать миграцию для таблицы chat_messages
- [ ] Реализовать UI компоненты чата (textarea, chat-input, chat-message, chat-interface)
- [ ] Создать floating chat button компонент
- [ ] Реализовать API client и типы для чата
- [ ] Реализовать сохранение истории в localStorage
- [ ] Интегрировать чат в dashboard page
- [ ] Реализовать responsive дизайн для mobile/desktop
- [ ] Тестирование и отладка всех компонентов
- [ ] Обновить документацию (roadmap, summary)