# ADR: Frontend Technology Stack

> **Status:** Accepted  
> **Date:** 2025-10-17  
> **Sprint:** F02 - Frontend Initialization

---

## Context

Для проекта **systech-aidd** требуется разработать современный веб-интерфейс для визуализации статистики Telegram-бота и предоставления AI-ассистента администратору. Необходимо выбрать оптимальный технологический стек, который обеспечит:

- **Production-ready решение** для dashboard приложения
- **Developer Experience** - удобная разработка и поддержка
- **Performance** - быстрая загрузка и отзывчивость
- **Type Safety** - минимизация runtime ошибок
- **Modern UI** - современный дизайн с минимальными усилиями
- **Scalability** - возможность расширения функциональности

### Требования

**Функциональные:**
- Dashboard со статистикой (графики, карточки, таблицы)
- AI-чат интерфейс (будущее)
- Responsive дизайн (desktop + mobile)
- Интеграция с REST API

**Нефункциональные:**
- TypeScript для type safety
- SSR/SSG для SEO и производительности
- Минимальный bundle size
- Быстрая разработка (MVP подход)
- Простота поддержки

---

## Decision

Принято решение использовать следующий технологический стек:

### Core Stack

1. **Framework:** Next.js 15
2. **UI Library:** React 19
3. **Language:** TypeScript (strict mode)
4. **Styling:** Tailwind CSS
5. **UI Components:** shadcn/ui
6. **Package Manager:** pnpm

### Development Tools

- **Linter:** ESLint (Next.js config + TypeScript)
- **Formatter:** Prettier (с Tailwind plugin)
- **Build Tool:** Next.js (встроенный Webpack/Turbopack)

---

## Rationale

### 1. Next.js 15

**Почему выбран:**

✅ **App Router (React Server Components)**
- Server Components по умолчанию → меньше JavaScript на клиенте
- Client Components только где нужна интерактивность
- Оптимальная производительность для dashboard приложения

✅ **SSR/SSG возможности**
- Server-Side Rendering для динамических данных
- Static Generation для статических страниц
- Incremental Static Regeneration (ISR) для кэширования

✅ **Built-in оптимизации**
- Automatic code splitting
- Image optimization (next/image)
- Font optimization (next/font)
- Route prefetching

✅ **Developer Experience**
- File-based routing (интуитивно)
- Fast Refresh (мгновенное обновление)
- TypeScript из коробки
- Отличная документация

✅ **Production-ready**
- Используется крупными компаниями (Vercel, Netflix, TikTok)
- Активное развитие и поддержка
- Огромное сообщество

**Альтернативы рассмотрены:**
- **Vite + React Router:** Хорош, но нет SSR из коробки, нужна дополнительная настройка
- **Remix:** Отличный SSR, но меньше экосистема и сообщество
- **Gatsby:** Фокус на static sites, избыточен для dashboard

**Почему Next.js лучше:**
- SSR + SSG из коробки без настройки
- App Router с React Server Components - современный подход
- Лучший DX среди React frameworks

---

### 2. React 19

**Почему выбран:**

✅ **React Server Components**
- Рендеринг на сервере без отправки кода клиенту
- Идеально для dashboard (статические карточки на сервере, графики на клиенте)
- Меньший bundle size

✅ **Улучшенная производительность**
- Automatic batching
- Transitions API
- Suspense для data fetching

✅ **Стабильность**
- Зрелая библиотека с огромным сообществом
- Обратная совместимость
- Отличная документация

**Альтернативы рассмотрены:**
- **Vue 3:** Хорош, но экосистема UI компонентов (shadcn/ui) заточена под React
- **Svelte:** Интересный, но меньше готовых решений для dashboard
- **Solid.js:** Производительный, но незрелая экосистема

**Почему React 19 лучше:**
- Server Components = performance win
- Огромная экосистема компонентов
- Команда знакома с React

---

### 3. TypeScript (strict mode)

**Почему выбран:**

✅ **Type Safety**
- Catch errors at compile time
- Autocomplete и IntelliSense в IDE
- Рефакторинг с уверенностью

✅ **Developer Experience**
- Документация через типы
- Легче onboarding новых разработчиков
- Меньше runtime ошибок

✅ **API интеграция**
- Типизированные API responses
- Синхронизация с backend типами (Pydantic → TypeScript)

✅ **Strict mode**
- Максимальная строгость проверки типов
- `noUncheckedIndexedAccess`, `noUnusedLocals`, `noUnusedParameters`
- Подход как в Python с mypy strict

**Альтернативы рассмотрены:**
- **JavaScript:** Быстрее писать код, но больше runtime ошибок
- **Flow:** Устаревает, меньше поддержки

**Почему TypeScript strict лучше:**
- Стандарт в современной разработке
- Особенно важен для team projects
- Совпадает с философией backend (Python + mypy strict)

---

### 4. Tailwind CSS

**Почему выбран:**

✅ **Utility-First подход**
- Быстрая разработка UI без написания CSS
- Консистентный дизайн (spacing, colors из конфига)
- Нет naming конфликтов (нет CSS классов)

✅ **Performance**
- PurgeCSS встроен → минимальный CSS bundle
- Только используемые стили попадают в production
- JIT режим (Just-In-Time) для dev скорости

✅ **Responsive Design**
- Mobile-first подход из коробки
- Breakpoints: `sm:`, `md:`, `lg:`, `xl:`
- Легко адаптировать под любые устройства

✅ **Dark Mode**
- Встроенная поддержка (`dark:` prefix)
- Легко добавить в будущем

✅ **Developer Experience**
- Autocomplete в IDE (Tailwind IntelliSense)
- Читаемый код (классы описывают стили)
- Нет переключения между файлами

**Альтернативы рассмотрены:**
- **CSS Modules:** Хороши, но медленнее разработка, нужно придумывать имена классов
- **Styled Components:** Runtime overhead, сложнее SSR
- **CSS-in-JS (Emotion):** Похоже на Styled Components, те же проблемы
- **Bootstrap:** Устаревший подход, тяжелый, сложно кастомизировать

**Почему Tailwind лучше:**
- Самый быстрый способ верстки в 2025
- Отличная интеграция с Next.js и shadcn/ui
- Минимальный bundle size в production

---

### 5. shadcn/ui

**Почему выбран:**

✅ **Copy-Paste компоненты**
- НЕ npm package → полный контроль над кодом
- Код компонентов в проекте → можно модифицировать
- Нет vendor lock-in

✅ **Tailwind-based**
- Стилизация через Tailwind классы
- Легко кастомизировать внешний вид
- Консистентный дизайн с остальным приложением

✅ **Accessibility**
- Построен на Radix UI primitives
- ARIA атрибуты из коробки
- Keyboard navigation
- Screen reader support

✅ **Качество компонентов**
- Продуманные API
- TypeScript типы
- Responsive дизайн
- Dark mode support

✅ **Готовые компоненты для Dashboard**
- Card, Button, Input, Label (базовые)
- Table, Chart, Select, Badge (для Sprint F03)
- Dialog, Sheet, Dropdown (для будущего)

**Альтернативы рассмотрены:**
- **Material UI (MUI):** Тяжелый, сложно кастомизировать, не Tailwind
- **Ant Design:** Китайский дизайн, тяжелый, сложная кастомизация
- **Chakra UI:** Хорош, но runtime CSS-in-JS = performance overhead
- **Headless UI:** Минималистичен, но нужно стилизовать все самим
- **Radix UI:** Primitives хороши, но shadcn/ui = Radix + готовые стили

**Почему shadcn/ui лучше:**
- Лучший баланс: готовые компоненты + полный контроль
- Идеальная интеграция с Tailwind и Next.js
- Быстрый старт (CLI для установки компонентов)
- Современный подход (2024-2025 стандарт)

---

### 6. pnpm

**Почему выбран:**

✅ **Производительность**
- Быстрее npm/yarn в 2-3 раза
- Hard links вместо копирования файлов
- Эффективный cache

✅ **Disk Space Efficiency**
- Один пакет = одна копия на диске (для всех проектов)
- Экономия гигабайтов дискового пространства
- Content-addressable storage

✅ **Строгость**
- Нет phantom dependencies (доступны только declared deps)
- Строгая изоляция пакетов
- Меньше конфликтов

✅ **Совместимость**
- Работает с npm registry
- Поддержка workspaces (для monorepo в будущем)
- Та же семантика что npm (install, add, remove)

**Альтернативы рассмотрены:**
- **npm:** Медленный, занимает много места
- **yarn (classic):** Устаревает, yarn berry сложен
- **yarn berry (v2+):** PnP подход экспериментальный, не все пакеты работают

**Почему pnpm лучше:**
- Самый быстрый и эффективный в 2025
- Строгость предотвращает ошибки
- Команда использует pnpm для backend тоже (консистентность)

---

## Consequences

### Положительные

✅ **Быстрая разработка**
- Next.js + shadcn/ui = MVP за несколько дней
- Tailwind = верстка без CSS файлов
- TypeScript = меньше отладки

✅ **Production-Ready**
- SSR/SSG для производительности
- Оптимизации Next.js из коробки
- Accessibility через shadcn/ui

✅ **Maintainability**
- TypeScript strict = понятный код
- shadcn/ui copy-paste = полный контроль
- Tailwind = консистентные стили

✅ **Developer Experience**
- Hot reload (Fast Refresh)
- TypeScript IntelliSense
- Tailwind autocomplete
- Отличная документация

✅ **Performance**
- React Server Components → меньше JS
- Tailwind PurgeCSS → минимальный CSS
- Next.js optimizations → fast loading

### Риски и митигации

⚠️ **Риск: Next.js 15 + React 19 = bleeding edge**
- **Митигация:** Использовать stable releases, тестировать после установки
- **Обоснование:** Преимущества Server Components перевешивают риск

⚠️ **Риск: shadcn/ui = код в проекте (не npm)**
- **Митигация:** Обновления через CLI, контроль изменений через git
- **Обоснование:** Полный контроль важнее автообновлений

⚠️ **Риск: Tailwind = много классов в JSX**
- **Митигация:** Извлекать компоненты, использовать @apply для повторов
- **Обоснование:** Читаемость улучшается с привычкой

⚠️ **Риск: pnpm = не все CI/CD поддерживают**
- **Митигация:** Vercel и GitHub Actions поддерживают pnpm
- **Обоснование:** Стандартные платформы работают без проблем

### Trade-offs

**Сложность vs Гибкость:**
- Next.js добавляет абстракции (vs Vite)
- **Выбор:** Готовые решения (SSR, routing) важнее простоты

**Bundle Size vs Developer Experience:**
- shadcn/ui = больше кода в проекте (vs npm package)
- **Выбор:** Контроль и кастомизация важнее размера репозитория

**Learning Curve vs Productivity:**
- Tailwind требует привыкания (vs Bootstrap)
- **Выбор:** Долгосрочная продуктивность важнее начального обучения

---

## Implementation Notes

### Порядок настройки (Sprint F02)

1. **Next.js 15** - `pnpm create next-app` с TypeScript, Tailwind, ESLint, App Router
2. **shadcn/ui** - `pnpm dlx shadcn@latest init` + базовые компоненты
3. **TypeScript** - strict mode в tsconfig.json
4. **Prettier** - форматирование с Tailwind plugin
5. **Structure** - создание директорий (components, lib, types)

### Версии (на момент Sprint F02)

- Next.js: 15.x (latest stable)
- React: 19.x
- TypeScript: 5.x
- Tailwind CSS: 3.x
- shadcn/ui: latest (CLI-based)
- pnpm: 8.x

### Будущие обновления

- **Sprint F03:** Добавление chart библиотеки (recharts/chart.js)
- **Sprint F04:** WebSocket для AI chat (если нужен real-time)
- **Sprint F05:** Авторизация (NextAuth.js или custom JWT)

---

## References

### Документация

- [Next.js 15 Documentation](https://nextjs.org/docs)
- [React 19 Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [pnpm Documentation](https://pnpm.io)

### Comparison Articles

- Next.js vs Remix vs Gatsby (2024)
- Tailwind CSS vs CSS-in-JS Performance
- shadcn/ui vs Material UI vs Ant Design

### Team Knowledge

- Backend использует: Python + FastAPI + TypeScript-like подход (Pydantic + mypy strict)
- Команда знакома с: React, TypeScript
- Infrastructure: Vercel (оптимален для Next.js) или Docker

---

## Status

- **Status:** ✅ Accepted
- **Date:** 2025-10-17
- **Sprint:** F02 - Frontend Initialization
- **Decision Maker:** systech-aidd team
- **Supersedes:** N/A (первое архитектурное решение для frontend)
- **Next Review:** После Sprint F03 (review chart library выбор)

---

## Changelog

- **2025-10-17:** Initial ADR creation (Sprint F02)

