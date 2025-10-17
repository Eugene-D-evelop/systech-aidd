# Dashboard Requirements - systech-aidd

> **Статус:** Активный документ  
> **Версия:** 1.0  
> **Дата:** 2025-10-17  
> **Sprint:** F03

---

## 1. Цель Dashboard

Визуализация статистики использования AI-бота через Telegram с удобным интерфейсом для администратора, основанным на данных из Mock API (Sprint F01).

---

## 2. Референс дизайна

**Базовый референс:** [shadcn/ui Dashboard-01](https://ui.shadcn.com/blocks#dashboard-01)

**Ключевые элементы дизайна:**
- Темная тема с минималистичным стилем
- Метрические карточки с индикаторами изменений (↑/↓ стрелки, проценты)
- Area chart для отображения временных рядов активности
- Фильтры периодов (7 дней / 30 дней / Всё время)
- Responsive grid layout

---

## 3. Источник данных

### Mock API Endpoint
```
GET http://localhost:8000/api/stats/dashboard
```

### Структура данных (из Sprint F01)

```typescript
interface DashboardStats {
  overview: {
    total_users: number
    active_users_7d: number
    active_users_30d: number
    total_messages: number
    messages_7d: number
    messages_30d: number
  }
  users: {
    premium_count: number
    premium_percentage: number
    regular_count: number
    by_language: { [key: string]: number }
  }
  messages: {
    avg_length: number
    first_message_date: string
    last_message_date: string
    user_to_assistant_ratio: number
  }
  metadata: {
    generated_at: string
    is_mock: boolean
  }
}
```

---

## 4. Метрики для отображения

### 4.1 Основные метрические карточки (Overview Stats)

#### Карточка 1: Total Users
- **Значение:** `overview.total_users`
- **Описание:** "Всего пользователей бота"
- **Индикатор изменения:** Рассчитывается на основе `active_users_30d` vs `total_users`
- **Формат:** Число без десятичных знаков

#### Карточка 2: Active Users (7d)
- **Значение:** `overview.active_users_7d`
- **Описание:** "Активных за 7 дней"
- **Индикатор изменения:** Сравнение 7d vs 30d активности
- **Формат:** Число + процент изменения

#### Карточка 3: Total Messages
- **Значение:** `overview.total_messages`
- **Описание:** "Всего сообщений"
- **Индикатор изменения:** `messages_7d` vs `messages_30d` trend
- **Формат:** Число с разделителями тысяч

#### Карточка 4: Avg Message Length
- **Значение:** `messages.avg_length`
- **Описание:** "Средняя длина сообщения"
- **Индикатор:** Статическое значение (без изменения)
- **Формат:** Число + " символов"

### 4.2 Индикаторы изменений

**Формула расчета:**
```typescript
// Для Active Users
const change7dVs30d = ((active_users_7d * 30 / 7) - active_users_30d) / active_users_30d * 100

// Для Messages
const changeMessagesVs30d = ((messages_7d * 30 / 7) - messages_30d) / messages_30d * 100
```

**Отображение:**
- ↑ зеленая стрелка + процент (если изменение положительное)
- ↓ красная стрелка + процент (если изменение отрицательное)
- Нет стрелки (если нет данных для сравнения)

---

## 5. Визуализации

### 5.1 Activity Chart (Area Chart)

**Тип:** Recharts AreaChart с градиентной заливкой

**Данные:** Временной ряд активности пользователей и сообщений

**Источник данных:**
- Mock данные генерируются на клиенте (функция `generateActivityData`)
- В Sprint F05: Real time-series данные из API

**Структура данных:**
```typescript
interface ActivityDataPoint {
  date: string // "Jan 1", "Jan 2", ...
  users: number
  messages: number
}
```

**Визуальные элементы:**
- 2 area кривые: users (синяя), messages (зеленая)
- Градиентная заливка под кривыми
- Tooltip при hover с данными
- X-axis: даты
- Y-axis: числовые значения
- Grid lines для читаемости

**Периоды фильтрации:**
- 7 дней: 7 точек данных (daily)
- 30 дней: 30 точек данных (daily)
- 90 дней (Всё время): 90 точек данных (daily)

### 5.2 User Distribution Chart (Bar Chart + Pie Chart)

#### A. Language Distribution (Bar Chart)

**Тип:** Recharts BarChart (горизонтальный)

**Данные:** `users.by_language`

**Пример данных:**
```typescript
[
  { language: "ru", count: 186 },
  { language: "en", count: 78 },
  { language: "uk", count: 15 },
  { language: "other", count: 8 }
]
```

**Визуальные элементы:**
- Горизонтальные бары с цветовым кодированием
- Label с названием языка
- Tooltip с количеством пользователей
- Сортировка по убыванию count

#### B. Premium vs Regular (Pie/Donut Chart)

**Тип:** Recharts PieChart (Donut style)

**Данные:** 
- `users.premium_count`
- `users.regular_count`
- `users.premium_percentage`

**Структура:**
```typescript
[
  { name: "Premium", value: premium_count, percentage: premium_percentage },
  { name: "Regular", value: regular_count, percentage: 100 - premium_percentage }
]
```

**Визуальные элементы:**
- Donut chart с центральным текстом (total users)
- 2 сегмента: Premium (gold/yellow), Regular (gray)
- Legend с процентами
- Tooltip с абсолютными значениями

---

## 6. Интерактивность

### 6.1 Period Filter

**Тип компонента:** Tabs (shadcn/ui)

**Варианты:**
- "7 дней" - `period: '7d'`
- "30 дней" - `period: '30d'`
- "Всё время" - `period: '90d'` (3 месяца для mock)

**Поведение:**
- Переключение обновляет данные в Activity Chart
- Метрические карточки статичны (показывают текущие данные из API)
- Сохранение выбранного периода в state (useState)

### 6.2 Loading States

**Skeleton UI:**
- Карточки метрик: прямоугольные skeleton блоки
- График: большой skeleton блок
- Анимация pulse effect

**Реализация:** `app/dashboard/loading.tsx`

### 6.3 Error States

**Сценарии ошибок:**
- API недоступен
- Network timeout
- Invalid response

**UI:**
- Error Card с сообщением
- Retry кнопка
- Инструкция запуска Mock API (если is_mock)

---

## 7. Responsive Design

### Breakpoints (Tailwind CSS)

#### Mobile (< 640px)
- Метрические карточки: 1 колонка (stack)
- Activity chart: Full width, уменьшенная высота
- Distribution charts: Stack vertically

#### Tablet (640-1024px)
- Метрические карточки: 2 колонки
- Activity chart: Full width
- Distribution charts: 2 колонки

#### Desktop (1024px+)
- Метрические карточки: 4 колонки
- Activity chart: Full width, увеличенная высота
- Distribution charts: 2 колонки

### Grid Layout

```tsx
// Stats Cards
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

// Charts Section
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
```

---

## 8. Mapping: API → UI Components

| API Field | UI Component | Описание |
|-----------|--------------|----------|
| `overview.total_users` | StatsCard #1 | Total Users |
| `overview.active_users_7d` | StatsCard #2 | Active Users (7d) |
| `overview.total_messages` | StatsCard #3 | Total Messages |
| `messages.avg_length` | StatsCard #4 | Avg Message Length |
| `overview.messages_7d` + `messages_30d` | StatsCard #3 indicator | Trend calculation |
| Mock time-series | ActivityChart | Generated client-side |
| `users.by_language` | BarChart | Language Distribution |
| `users.premium_count` + `regular_count` | PieChart | Premium vs Regular |
| `metadata.is_mock` | Badge | "(Mock Data)" indicator |

---

## 9. Технические требования

### 9.1 Производительность
- **LCP** < 2.5s (Largest Contentful Paint)
- **FID** < 100ms (First Input Delay)
- **Bundle size:** Recharts lazy loading при необходимости

### 9.2 Типизация
- TypeScript strict mode
- Все пропсы компонентов типизированы
- 0 TypeScript ошибок

### 9.3 Качество кода
- ESLint: 0 errors
- Prettier: Consistent formatting
- Accessibility: ARIA labels для графиков

### 9.4 Компоненты

#### Server Components
- `app/dashboard/page.tsx` - Загрузка данных из Mock API

#### Client Components
- `components/dashboard/stats-card.tsx` - Статичные, но можно сделать client для анимаций
- `components/dashboard/activity-chart.tsx` - Client (recharts)
- `components/dashboard/user-distribution-chart.tsx` - Client (recharts)
- `components/dashboard/period-filter.tsx` - Client (state management)

---

## 10. Зависимости

### NPM Packages
- `recharts` ~2.x - Charting library
- `date-fns` ~3.x - Date formatting

### shadcn/ui Components
- `chart` - Recharts wrappers с темизацией
- `badge` - Индикаторы статуса
- `tabs` - Period filter
- `select` - Будущие фильтры (опционально)
- `card`, `button`, `input`, `label` - Уже установлены в Sprint F02

---

## 11. Будущие улучшения (Post-Sprint F03)

### Sprint F05: Real API Integration
- Replace mock time-series с реальными данными из БД
- Добавить endpoint для time-series: `GET /api/stats/activity?period=7d`
- Кэширование данных (ISR или SWR)

### Дополнительные фичи
- Export данных (CSV, PDF)
- Real-time updates (WebSocket)
- Customizable dashboard (drag-and-drop widgets)
- Сравнение периодов (compare mode)
- Drill-down в детальную статистику

---

## 12. Acceptance Criteria

Sprint F03 считается завершенным, когда:

- ✅ Dashboard отображает 4 метрические карточки с данными из Mock API
- ✅ Индикаторы изменений (стрелки ↑/↓) работают корректно
- ✅ Activity chart показывает area chart с mock time-series данными
- ✅ User distribution charts (bar + pie) отображают данные из API
- ✅ Period фильтры (7d/30d/90d) переключают данные в Activity chart
- ✅ Loading skeleton UI отображается при загрузке
- ✅ Error handling работает с retry функциональностью
- ✅ Responsive дизайн работает на всех breakpoints
- ✅ TypeScript: 0 ошибок (strict mode)
- ✅ ESLint: 0 ошибок
- ✅ UI визуально соответствует референсу shadcn/ui dashboard-01

---

**Создан:** 2025-10-17 (Sprint F03)  
**Следующее обновление:** После Sprint F05 (Real API integration)

