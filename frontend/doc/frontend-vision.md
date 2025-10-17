# Frontend Vision: systech-aidd

> **Версия:** 1.0  
> **Дата:** 2025-10-17  
> **Статус:** Активный документ

---

## 1. Цель и назначение

Frontend приложение **systech-aidd** - современный веб-интерфейс для управления и мониторинга AI-бота через Telegram. Приложение предоставляет администраторам удобный доступ к статистике использования бота и интерактивный AI-чат для анализа данных.

### Основные задачи

- **Визуализация статистики** - отображение метрик использования бота в удобном формате
- **AI-ассистент для администратора** - интерфейс для вопросов по статистике через Text2SQL
- **Управление данными** - просмотр и анализ информации о пользователях и диалогах
- **Responsive UI** - адаптивный интерфейс для desktop и mobile устройств

---

## 2. Архитектура приложения

### 2.1 Технологический стек

- **Framework:** Next.js 15 (App Router)
- **UI Library:** React 19
- **Язык:** TypeScript (strict mode)
- **Стилизация:** Tailwind CSS
- **Компоненты:** shadcn/ui
- **Пакетный менеджер:** pnpm
- **Линтеры:** ESLint + Prettier

### 2.2 Архитектурные принципы

#### KISS (Keep It Simple, Stupid)
- Минимум абстракций
- Простые и понятные решения
- Стандартные подходы Next.js

#### Type Safety First
- TypeScript strict mode для всего кода
- Полная типизация API responses
- Статическая проверка типов (mypy-подобный подход)

#### Component-Driven Development
- Переиспользуемые UI компоненты
- Композиция вместо наследования
- shadcn/ui как основа

#### Server-First Architecture
- React Server Components по умолчанию
- Client Components только где необходимо (интерактивность)
- Минимизация JavaScript на клиенте

---

## 3. Структура проекта

```
frontend/
├── public/                    # Статические файлы
│   ├── favicon.ico
│   └── images/
├── src/
│   ├── app/                   # Next.js App Router
│   │   ├── layout.tsx        # Root layout
│   │   ├── page.tsx          # Home (redirect → /dashboard)
│   │   ├── dashboard/        # Dashboard страница
│   │   │   └── page.tsx
│   │   └── (future: chat/)   # AI Chat (Sprint F04)
│   ├── components/           # React компоненты
│   │   ├── ui/              # shadcn/ui компоненты
│   │   ├── dashboard/       # Dashboard компоненты
│   │   └── layout/          # Layout компоненты (Header, Footer)
│   ├── lib/                  # Утилиты и хелперы
│   │   ├── utils.ts         # shadcn/ui utilities
│   │   └── api.ts           # API client
│   ├── types/                # TypeScript типы
│   │   └── stats.ts         # API response types
│   └── styles/               # Глобальные стили
│       └── globals.css      # Tailwind CSS imports
├── .env.local                # Environment variables (gitignored)
├── .env.example              # Example env variables
├── components.json           # shadcn/ui config
├── tailwind.config.ts        # Tailwind config
├── tsconfig.json             # TypeScript config
├── next.config.js            # Next.js config
└── package.json              # Dependencies
```

---

## 4. Основные страницы

### 4.1 Home Page (`/`)

**Назначение:** Точка входа в приложение

**Функциональность:**
- Автоматический redirect на `/dashboard`
- Или Welcome screen с описанием (опционально в будущем)

**Реализация:** Server Component, простой redirect

### 4.2 Dashboard (`/dashboard`)

**Назначение:** Визуализация статистики использования бота

**Функциональность:**
- Карточки с основными метриками (total users, messages, activity)
- Графики активности (временные ряды)
- Распределение пользователей (Premium, языки)
- Статистика сообщений (длина, соотношения)
- Фильтрация по периодам (7 дней, 30 дней, all time)
- Responsive grid layout

**Компоненты:**
- `StatsOverviewCard` - карточка с метрикой
- `ActivityChart` - график активности
- `UserDistributionChart` - диаграмма распределения
- `DashboardFilters` - фильтры периодов

**Реализация:** Server Component для начальной загрузки, Client Components для интерактивности

### 4.3 AI Chat (`/chat`) - Sprint F04

**Назначение:** Интерфейс для вопросов администратора по статистике

**Функциональность:**
- Chat интерфейс с LLM
- Text2SQL: вопросы на естественном языке → SQL запросы
- Отображение результатов запросов
- История чата в рамках сессии
- Quick suggestions (примеры вопросов)

**Реализация:** Client Component (интерактивный chat)

---

## 5. Компонентная архитектура

### 5.1 Типы компонентов

#### Server Components (по умолчанию)
- Страницы (page.tsx)
- Layout компоненты
- Статические карточки
- Компоненты без state

**Преимущества:**
- Меньше JavaScript на клиенте
- Доступ к backend напрямую
- Лучше SEO

#### Client Components ('use client')
- Интерактивные элементы (кнопки, формы)
- Компоненты с useState, useEffect
- Chart компоненты
- AI Chat интерфейс

**Когда использовать:**
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- State management (useState, useReducer)
- Effects (useEffect, useLayoutEffect)

### 5.2 Стратегия композиции

```
Page (Server Component)
├── Layout (Server Component)
│   ├── Header (Server Component)
│   └── Footer (Server Component)
└── Content
    ├── StaticCards (Server Component)
    └── InteractiveChart (Client Component)
        └── ChartLib (Client Component)
```

**Принцип:** Server Components оборачивают Client Components, но не наоборот

---

## 6. State Management

### 6.1 Подход

**Минималистичный подход без внешних библиотек:**
- **Server state:** React Server Components + fetch
- **Client state:** useState + useReducer
- **URL state:** Next.js searchParams
- **Form state:** React Hook Form (если понадобится)

### 6.2 Когда НЕ нужен Redux/Zustand

- ✅ Simple dashboard с независимыми виджетами
- ✅ Server-first architecture
- ✅ Minimal client-side state
- ✅ MVP фаза проекта

**Текущее решение:** Локальный state в компонентах + Server Components для данных

---

## 7. API интеграция

### 7.1 Mock API (Sprint F01-F03)

**Endpoint:** `http://localhost:8000/api/stats/dashboard`

**Клиент:** `src/lib/api.ts`

```typescript
export async function getDashboardStats() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const response = await fetch(`${apiUrl}/api/stats/dashboard`, {
    cache: 'no-store' // Always fresh data
  })
  if (!response.ok) {
    throw new Error('Failed to fetch stats')
  }
  return response.json()
}
```

**Стратегия кэширования:**
- `cache: 'no-store'` - всегда свежие данные для статистики
- В будущем: ISR (Incremental Static Regeneration) с revalidate

### 7.2 Real API (Sprint F05)

**Изменения:**
- Подключение к реальной БД через StatCollector
- Добавление авторизации (JWT tokens)
- Rate limiting
- Error handling и retry logic

**Обратная совместимость:** API контракт остается тот же, меняется только backend

---

## 8. Роутинг (Next.js App Router)

### 8.1 Структура маршрутов

```
/                    → Home (redirect to /dashboard)
/dashboard           → Dashboard страница
/chat               → AI Chat (Sprint F04)
```

### 8.2 Преимущества App Router

- **File-based routing** - интуитивная структура
- **Layouts** - переиспользуемые layouts с вложенностью
- **Loading states** - `loading.tsx` для Suspense
- **Error handling** - `error.tsx` для error boundaries
- **Server Components** - по умолчанию

### 8.3 Navigation

**Header компонент:**
- Link to `/dashboard`
- Link to `/chat` (когда реализован)
- Highlight активной страницы

**Реализация:** `next/link` для client-side navigation

---

## 9. Стилизация (Tailwind CSS + shadcn/ui)

### 9.1 Tailwind CSS

**Преимущества:**
- Utility-first подход
- Минимальный CSS bundle (PurgeCSS)
- Responsive design из коробки
- Dark mode support (будущее)

**Конфигурация:** `tailwind.config.ts`

```typescript
theme: {
  extend: {
    colors: {
      // shadcn/ui theme colors
    }
  }
}
```

### 9.2 shadcn/ui

**Философия:** Copy-paste компоненты (не npm package)

**Преимущества:**
- Полный контроль над кодом компонентов
- Customizable через Tailwind
- Accessibility из коробки (Radix UI)
- Consistent design system

**Базовые компоненты (Sprint F02):**
- Button
- Card
- Input
- Label

**Будущие компоненты (Sprint F03):**
- Chart (через recharts)
- Table
- Select
- Badge
- Tabs

---

## 10. UI/UX принципы

### 10.1 Responsive Design

**Breakpoints (Tailwind):**
- `sm`: 640px (tablet)
- `md`: 768px (small desktop)
- `lg`: 1024px (desktop)
- `xl`: 1280px (large desktop)

**Mobile-first approach:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Cards */}
</div>
```

### 10.2 Accessibility (a11y)

**Требования:**
- Semantic HTML
- ARIA labels где необходимо
- Keyboard navigation
- Screen reader support (shadcn/ui built-in)
- Contrast ratio WCAG AA minimum

**Target:** WCAG 2.1 Level AA

### 10.3 Performance

**Метрики:**
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **Lighthouse Score**: 90+

**Оптимизации:**
- Next.js Image optimization
- Code splitting (automatic в Next.js)
- Server Components (меньше JS)
- Lazy loading для charts

### 10.4 Design System

**Цветовая палитра:** Slate (neutral) от shadcn/ui

**Типографика:** Inter font (Next.js font optimization)

**Spacing:** Tailwind spacing scale (4px grid)

**Consistency:** shadcn/ui компоненты как single source of truth

---

## 11. Качество кода

### 11.1 TypeScript

**Конфигурация:** `tsconfig.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

**Цель:** 100% type coverage, zero `any` types

### 11.2 Линтеры

**ESLint:**
- Next.js recommended
- TypeScript ESLint
- React Hooks rules
- Import sorting

**Prettier:**
- Consistent formatting
- Tailwind plugin (class sorting)

**Pre-commit:** Будущее - Husky + lint-staged

### 11.3 Тестирование

**Сейчас (Sprint F02):** Ручное тестирование

**Будущее:**
- **Unit tests:** Vitest + React Testing Library
- **E2E tests:** Playwright
- **Coverage target:** 70%+

---

## 12. Разработка и Deployment

### 12.1 Development

**Команды:**
```bash
pnpm install       # Установка зависимостей
pnpm dev           # Dev server (localhost:3000)
pnpm build         # Production build
pnpm start         # Production server
pnpm lint          # ESLint check
pnpm format        # Prettier format
pnpm type-check    # TypeScript check
```

**Dev server:** Hot reload, Fast Refresh, Error overlay

### 12.2 Build & Deploy

**Build процесс:**
1. TypeScript compilation
2. Tailwind CSS purge
3. Next.js optimization
4. Static generation где возможно

**Deployment target:** Vercel (optimal для Next.js) или Docker

**Environment variables:**
- `NEXT_PUBLIC_API_URL` - URL Mock/Real API
- (Будущее: `NEXT_PUBLIC_AUTH_DOMAIN`, etc.)

---

## 13. Следующие шаги

### Sprint F03: Dashboard UI

- Реализация всех компонентов дашборда
- Интеграция графиков (recharts)
- Responsive layout
- Loading и error states
- Фильтрация данных

### Sprint F04: AI Chat

- Chat UI компонент
- WebSocket или REST для chat
- Text2SQL интеграция
- Message history
- Quick suggestions

### Sprint F05: Real API

- Переход с Mock на Real API
- Авторизация (JWT)
- Error handling
- Rate limiting
- Monitoring

---

## 14. Принципы поддержки документа

Этот документ - **живой**, обновляется по мере развития проекта:

- ✅ **Актуализация:** После каждого спринта
- ✅ **Версионность:** Semantic versioning (1.0, 1.1, 2.0)
- ✅ **Консистентность:** С кодом и ADR документами
- ✅ **Простота:** KISS принцип в документации

---

**Создан:** 2025-10-17 (Sprint F02)  
**Следующее обновление:** После Sprint F03  
**Владелец:** systech-aidd team

