# Frontend: systech-aidd

> **Статус:** ✅ Инициализирован (Sprint F02)  
> **Версия:** 0.1.0

---

## 📋 Описание

Современный веб-интерфейс для управления и мониторинга AI-бота **systech-aidd**. Включает dashboard со статистикой диалогов и AI-чат для администратора с поддержкой Text2SQL запросов.

---

## 🚀 Технологический стек

### Core
- **Framework:** Next.js 15 (App Router)
- **UI Library:** React 19
- **Язык:** TypeScript (strict mode)
- **Пакетный менеджер:** pnpm

### Styling & UI
- **Styling:** Tailwind CSS 4
- **UI Components:** shadcn/ui
- **Fonts:** Inter (Google Fonts)

### Development Tools
- **Linter:** ESLint 9
- **Formatter:** Prettier + prettier-plugin-tailwindcss
- **Type Checking:** TypeScript 5.9 (strict mode)

---

## 🏗️ Структура проекта

```
frontend/
├── public/                    # Статические файлы
├── src/
│   ├── app/                   # Next.js App Router
│   │   ├── layout.tsx        # Root layout с Header
│   │   ├── page.tsx          # Home (redirect → /dashboard)
│   │   └── dashboard/        # Dashboard страница
│   │       └── page.tsx
│   ├── components/           # React компоненты
│   │   ├── ui/              # shadcn/ui компоненты
│   │   ├── dashboard/       # Dashboard компоненты
│   │   └── layout/          # Layout компоненты (Header)
│   ├── lib/                  # Утилиты и хелперы
│   │   ├── utils.ts         # shadcn/ui utilities
│   │   └── api.ts           # API client для Mock API
│   ├── types/                # TypeScript типы
│   │   └── stats.ts         # API response types
│   └── styles/               # Глобальные стили
│       └── globals.css      # Tailwind CSS
├── doc/                       # Документация
│   ├── frontend-vision.md    # Техническое видение
│   └── adr-tech-stack.md     # ADR с обоснованием стека
├── .env.local                # Environment variables (gitignored)
├── .env.example              # Example env variables
└── package.json              # Dependencies
```

---

## 🚀 Быстрый старт

### Установка зависимостей

```bash
# Из корня проекта
make frontend-install

# Или напрямую
cd frontend && pnpm install
```

### Запуск dev сервера

```bash
# Из корня проекта
make frontend-dev

# Или напрямую
cd frontend && pnpm dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

### Environment Variables

Создайте `.env.local` файл (или скопируйте из `.env.example`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📦 Доступные команды

### Через Makefile (из корня проекта)

```bash
make frontend-install      # Установка зависимостей
make frontend-dev          # Запуск dev server
make frontend-build        # Production build
make frontend-start        # Запуск production server
make frontend-lint         # ESLint проверка
make frontend-format       # Prettier форматирование
make frontend-type-check   # TypeScript проверка
```

### Напрямую (из директории frontend)

```bash
pnpm dev           # Запуск в режиме разработки
pnpm build         # Сборка продакшн версии
pnpm start         # Запуск продакшн версии
pnpm lint          # Проверка кода линтером
pnpm format        # Форматирование кода
pnpm tsc --noEmit  # Type checking
```

---

## 🔗 Интеграция с Backend

Frontend интегрирован с Mock API из Sprint F01:

- **Mock API endpoint:** `http://localhost:8000/api/stats/dashboard`
- **API Client:** `src/lib/api.ts`
- **Types:** `src/types/stats.ts` (синхронизированы с Pydantic моделями)

### Запуск Mock API

```bash
# Из корня проекта
make api-dev
```

API будет доступен на `http://localhost:8000`. Dashboard автоматически подключится к нему.

---

## 📊 Основные страницы

### Home Page (`/`)
Автоматический redirect на `/dashboard`.

### Dashboard (`/dashboard`)
Визуализация статистики использования бота:
- Карточки с основными метриками (пользователи, сообщения, активность)
- Распределение пользователей (Premium vs Regular)
- Статистика сообщений (временные метки, соотношения)
- Loading и error states

**Технологии:**
- React Server Components для начальной загрузки
- shadcn/ui Card компоненты
- Типизированные API requests

### AI Chat (Coming Soon)
Будет реализован в Sprint F04.

---

## 🎨 UI Components

### shadcn/ui компоненты

Установлены базовые компоненты (Sprint F02):
- **Button** - кнопки с вариантами стилей
- **Card** - карточки для метрик
- **Input** - поля ввода
- **Label** - метки для форм

Для добавления новых компонентов:

```bash
cd frontend
pnpm dlx shadcn@latest add [component-name]
```

### Кастомные компоненты

- **Header** - `src/components/layout/header.tsx`
- **Dashboard Cards** - встроены в `src/app/dashboard/page.tsx`

---

## 🧪 Тестирование

### Type Checking

```bash
make frontend-type-check
```

### Linting

```bash
make frontend-lint
```

### Formatting

```bash
make frontend-format
```

---

## 📖 Документация

### Техническая документация

- **Frontend Vision:** [doc/frontend-vision.md](doc/frontend-vision.md)
- **ADR Tech Stack:** [doc/adr-tech-stack.md](doc/adr-tech-stack.md)
- **Frontend Roadmap:** [../docs/frontend-roadmap.md](../docs/frontend-roadmap.md)

### TypeScript Конфигурация

- **Strict mode:** Включен
- **noUncheckedIndexedAccess:** Включен
- **noUnusedLocals:** Включен
- **noUnusedParameters:** Включен
- **Paths:** `@/*` → `./src/*`

### Prettier Конфигурация

- **Semi:** false
- **Single Quote:** true
- **Tab Width:** 2
- **Trailing Comma:** es5
- **Print Width:** 80
- **Plugin:** prettier-plugin-tailwindcss

---

## 🔮 Следующие шаги

### Sprint F03: Dashboard UI
- Полноценные графики (Chart.js/Recharts)
- Фильтрация данных по периодам
- Responsive design improvements
- Loading skeletons

### Sprint F04: AI Chat
- Chat интерфейс
- Text2SQL интеграция
- WebSocket или REST для real-time

### Sprint F05: Real API
- Переход с Mock на Real API
- Авторизация
- Error handling improvements

---

## 🤝 Contributing

### Code Style

- Следуйте TypeScript strict mode
- Используйте Prettier для форматирования
- Проверяйте lint перед коммитом
- Используйте shadcn/ui компоненты где возможно

### Архитектурные принципы

- **KISS** - минимум абстракций
- **Server-First** - используйте Server Components по умолчанию
- **Type Safety** - 100% типизация
- **Component-Driven** - переиспользуемые компоненты

---

## 📝 Метрики качества

### Целевые показатели

- ✅ **TypeScript strict mode:** 100%
- ✅ **ESLint:** 0 ошибок
- ✅ **Prettier:** Консистентный стиль
- 🎯 **Lighthouse Score:** 90+ (цель для Sprint F03)
- 🎯 **Bundle Size:** Оптимизирован (цель для Sprint F03)

---

## 🐛 Troubleshooting

### Mock API не отвечает

1. Убедитесь, что Mock API запущен:
   ```bash
   make api-dev
   ```

2. Проверьте `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. Перезапустите dev server:
   ```bash
   make frontend-dev
   ```

### Ошибки TypeScript

```bash
# Проверьте типы
make frontend-type-check

# Возможно нужно переустановить зависимости
cd frontend && rm -rf node_modules pnpm-lock.yaml && pnpm install
```

### Ошибки Prettier/ESLint

```bash
# Автофикс линтера
make frontend-lint --fix

# Форматирование
make frontend-format
```

---

## 📬 Контакты

**Проект:** systech-aidd  
**Sprint:** F02 - Frontend Initialization  
**Дата:** 2025-10-17  
**Статус:** ✅ Завершен
