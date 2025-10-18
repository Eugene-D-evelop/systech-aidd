<!-- 731e1f8d-d1af-450e-8f06-353d07809b35 aa5f039c-88c3-4f48-a8f8-850b66ba4ad9 -->
# План Спринта F03: Реализация Dashboard статистики диалогов

## Цель

Разработать полноценный dashboard для визуализации статистики диалогов AI-бота с интеграцией Mock API, графиками на recharts, фильтрацией периодов и современным UI на основе shadcn/ui dashboard-01 референса.

## Референс

- **Дизайн:** shadcn/ui dashboard-01 (предоставленный скриншот)
- **Ключевые элементы:** 
                - Метрические карточки с индикаторами изменений (↑/↓ стрелки, проценты)
                - Area chart для временных рядов
                - Фильтры периодов (Last 3 months, Last 30 days, Last 7 days)
                - Темная тема, минималистичный дизайн

## Основные изменения

### 1. Создание спецификации требований

**Файл:** `docs/dashboard-requirements.md`

Создать документ с функциональными требованиями к Dashboard:

- Список метрик для отображения (на основе Mock API данных из Sprint F01)
- Описание визуализаций (карточки, графики)
- Требования к интерактивности (фильтры периодов: 7d/30d/all)
- Референс дизайна (ссылка на shadcn/ui dashboard-01)
- Mapping Mock API данных на UI компоненты

### 2. Установка зависимостей

**Команды для установки:**

```bash
cd frontend
pnpm add recharts date-fns
npx shadcn@latest add chart
npx shadcn@latest add badge  
npx shadcn@latest add tabs
npx shadcn@latest add select
```

**Зависимости:**

- `recharts` для графиков (~80KB, industry standard)
- `date-fns` для форматирования дат
- shadcn/ui компоненты: chart, badge, tabs, select

**Файлы:** `frontend/package.json`, `components/ui/*`

### 2. Создание компонентов Dashboard

#### 2.1 StatsCard компонент (`components/dashboard/stats-card.tsx`)

Переиспользуемая карточка для отображения метрик с индикаторами изменений:

- Props: title, value, change (%), trend (up/down), description
- Стрелки ↑/↓ с цветовым кодированием (green/red)
- Адаптация под данные из Mock API

#### 2.2 ActivityChart компонент (`components/dashboard/activity-chart.tsx`)

Area chart для визуализации активности пользователей/сообщений:

- Recharts AreaChart с градиентной заливкой
- Двойная линия (пользователи + сообщения)
- Responsive дизайн
- Mock данные для временного ряда (будет генерироваться на клиенте)

#### 2.3 UserDistributionChart (`components/dashboard/user-distribution-chart.tsx`)

Визуализация распределения:

- Bar chart для языков пользователей
- Pie/Donut chart для Premium vs Regular
- Используем данные `users.by_language` и `users.premium_percentage`

#### 2.4 PeriodFilter компонент (`components/dashboard/period-filter.tsx`)

Фильтры периодов для дашборда:

- Tabs или Button Group с вариантами: 7 дней / 30 дней / Всё время
- State management через useState
- Адаптация данных на основе выбранного периода

### 3. Обновление Dashboard страницы (`app/dashboard/page.tsx`)

**Структура:**

```tsx
- Header секция (заголовок + описание)
- StatsCard grid (4 карточки: Total Users, Active Users, Total Messages, Avg Message Length)
  - Каждая с индикатором изменения (comparing 7d vs 30d data)
- PeriodFilter 
- ActivityChart (большой area chart, как на референсе)
- UserDistributionChart section (2 колонки: языки + premium distribution)
```

**Данные:**

- Server Component загружает данные из Mock API
- Передает данные в Client Components через props
- Client Components управляют интерактивностью (фильтры, графики)

### 4. Генерация mock time-series данных

**Файл:** `frontend/src/lib/mock-time-series.ts`

Утилита для генерации временных рядов на клиенте:

- Функция `generateActivityData(period: '7d' | '30d' | '90d')` 
- Возвращает массив `{ date: string, users: number, messages: number }`
- Реалистичные данные с трендами и вариациями

### 5. shadcn/ui компоненты

Установить через `npx shadcn@latest add`:

- `chart` - обертки для recharts с темами
- `badge` - для индикаторов статуса
- `tabs` - для фильтров периодов
- `select` - на будущее для дополнительных фильтров

### 6. Responsive дизайн

**Breakpoints:**

- Mobile (< 640px): 1 колонка для всех карточек
- Tablet (640-1024px): 2 колонки для StatsCard
- Desktop (1024px+): 4 колонки для StatsCard, 2 для charts

**Grid layout:** TailwindCSS classes `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4`

### 7. Loading и Error states

**Loading:**

- Skeleton компоненты для карточек и графиков
- Использовать `loading.tsx` в app/dashboard/

**Error:**

- Улучшить существующий error handling
- Добавить retry функциональность
- Friendly error messages

## Структура файлов

```
frontend/src/
├── app/dashboard/
│   ├── page.tsx                 # ✏️ Обновить - полноценный dashboard
│   └── loading.tsx              # ➕ Создать - skeleton UI
├── components/dashboard/
│   ├── stats-card.tsx           # ➕ Создать
│   ├── activity-chart.tsx       # ➕ Создать
│   ├── user-distribution-chart.tsx  # ➕ Создать
│   └── period-filter.tsx        # ➕ Создать
├── components/ui/
│   ├── badge.tsx                # ➕ Установить (shadcn)
│   ├── tabs.tsx                 # ➕ Установить (shadcn)
│   ├── chart.tsx                # ➕ Установить (shadcn)
│   └── select.tsx               # ➕ Установить (shadcn)
├── lib/
│   └── mock-time-series.ts      # ➕ Создать - генерация данных
└── types/
    └── stats.ts                 # (уже существует)
```

## Ключевые технические решения

1. **Server + Client Components:** Dashboard page - Server Component (загружает данные), графики - Client Components (интерактивность)
2. **Mock time-series:** Генерируем на клиенте для демонстрации, в Sprint F05 заменим на реальные данные из API
3. **Recharts:** Industry-standard библиотека, хорошо интегрируется с shadcn/ui через chart компонент
4. **Типизация:** Все пропсы компонентов строго типизированы, TypeScript strict mode
5. **Accessibility:** shadcn/ui компоненты из коробки доступны, добавим ARIA labels для графиков

## Критерии завершения

- ✅ Dashboard отображает 4 метрические карточки с индикаторами изменений
- ✅ Activity chart показывает временной ряд (area chart)
- ✅ User distribution charts отображают данные по языкам и Premium статусу
- ✅ Period фильтры работают и обновляют данные
- ✅ Responsive дизайн работает на mobile/tablet/desktop
- ✅ Loading states отображаются корректно
- ✅ Error handling работает с retry функциональностью
- ✅ Все TypeScript типы корректны (0 ошибок)
- ✅ ESLint проходит без ошибок
- ✅ UI соответствует референсу shadcn/ui dashboard-01

## Следующие шаги

- Sprint F04: Реализация AI-чата для администратора
- Sprint F05: Переход на Real API с интеграцией БД

### To-dos

- [ ] Установить зависимости: recharts, date-fns, shadcn/ui компоненты (chart, badge, tabs, select)
- [ ] Создать утилиту генерации mock time-series данных (lib/mock-time-series.ts)
- [ ] Создать компонент StatsCard с индикаторами изменений и стрелками
- [ ] Создать компонент ActivityChart с area chart на recharts
- [ ] Создать компонент UserDistributionChart с bar и pie charts
- [ ] Создать компонент PeriodFilter с tabs для фильтрации периодов
- [ ] Обновить Dashboard страницу с новыми компонентами и layout
- [ ] Добавить loading.tsx skeleton UI и улучшить error handling
- [ ] Финальная полировка responsive дизайна и тестирование на разных устройствах


