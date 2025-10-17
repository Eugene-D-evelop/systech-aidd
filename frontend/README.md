# 🎨 systech-aidd Frontend

> Modern web dashboard for AI Telegram bot monitoring and administration

**Tech Stack:** Next.js 15 + React 19 + TypeScript + shadcn/ui + Tailwind CSS + Recharts

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Commands](#-commands)
- [Documentation](#-documentation)

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- pnpm 8+
- Mock API running on `localhost:8000` (see [Backend README](../README.md))

### Installation

```bash
# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env.local

# Run development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) to see the dashboard.

---

## ✨ Features

### Dashboard (Sprint F03)

**Metrics Cards:**
- Total Users
- Active Users (7d) with change indicators
- Total Messages
- Messages (7d) with change indicators
- Average Message Length
- Premium Users percentage
- User to Assistant ratio

**Charts & Visualizations:**
- 📈 Activity Chart - Area chart with users and messages over time
- 📊 Language Distribution - Bar chart showing user language preferences
- 🥧 Premium Distribution - Pie chart showing Premium vs Regular users

**Interactivity:**
- Period filters (7 days / 30 days / 3 months)
- Responsive design (mobile/tablet/desktop)
- Loading skeleton states
- Error handling with retry

**UI/UX:**
- Modern dark theme (shadcn/ui dashboard-01 inspired)
- Trend indicators (↑/↓ arrows with color coding)
- Smooth animations and transitions
- Accessible components (WCAG AA)

---

## 🛠 Tech Stack

### Core

- **Framework:** [Next.js 15.5.6](https://nextjs.org/) (App Router)
- **UI Library:** [React 19.1.0](https://react.dev/)
- **Language:** [TypeScript 5.9.3](https://www.typescriptlang.org/) (strict mode)

### Styling

- **CSS Framework:** [Tailwind CSS 4.1.14](https://tailwindcss.com/)
- **Components:** [shadcn/ui](https://ui.shadcn.com/) (Radix UI primitives)
- **Icons:** [Lucide React 0.546.0](https://lucide.dev/)

### Data Visualization

- **Charts:** [Recharts 3.3.0](https://recharts.org/)
- **Date Utils:** [date-fns 4.1.0](https://date-fns.org/)

### Development Tools

- **Package Manager:** [pnpm 10.18.1](https://pnpm.io/)
- **Linter:** [ESLint 9.37.0](https://eslint.org/)
- **Formatter:** [Prettier 3.6.2](https://prettier.io/)

---

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── app/               # Next.js App Router
│   │   ├── layout.tsx    # Root layout with Header
│   │   ├── page.tsx      # Home (redirects to /dashboard)
│   │   └── dashboard/    # Dashboard pages
│   │       ├── page.tsx        # Dashboard (Server Component)
│   │       └── loading.tsx     # Loading skeleton
│   ├── components/
│   │   ├── ui/           # shadcn/ui components
│   │   │   ├── badge.tsx
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── chart.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   └── tabs.tsx
│   │   ├── dashboard/    # Dashboard-specific components
│   │   │   ├── dashboard-client.tsx      # Client wrapper
│   │   │   ├── stats-card.tsx            # Metric cards
│   │   │   ├── period-filter.tsx         # Period tabs
│   │   │   ├── activity-chart.tsx        # Area chart
│   │   │   └── user-distribution-chart.tsx  # Bar + Pie charts
│   │   └── layout/       # Layout components
│   │       └── header.tsx
│   ├── lib/              # Utilities
│   │   ├── api.ts               # API client
│   │   ├── utils.ts             # Tailwind cn helper
│   │   └── mock-time-series.ts  # Mock data generation
│   └── types/            # TypeScript types
│       └── stats.ts             # API response types
├── .env.local            # Environment variables (gitignored)
├── .env.example          # Example env file
├── components.json       # shadcn/ui config
├── next.config.ts        # Next.js config
├── tailwind.config.ts    # Tailwind config
├── tsconfig.json         # TypeScript config (strict mode)
└── package.json          # Dependencies
```

---

## ⚡ Commands

### Development

```bash
# Start dev server (http://localhost:3000)
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start
```

### Code Quality

```bash
# Run ESLint
pnpm lint

# Run Prettier
pnpm format

# Type check with TypeScript
pnpm tsc --noEmit
```

### Makefile (from project root)

```bash
# Install frontend dependencies
make frontend-install

# Run dev server
make frontend-dev

# Build
make frontend-build

# Lint
make frontend-lint

# Format
make frontend-format

# Type check
make frontend-type-check
```

---

## 📚 Documentation

### Project Documentation

- **[Frontend Vision](./doc/frontend-vision.md)** - Technical vision and architecture
- **[Tech Stack ADR](./doc/adr-tech-stack.md)** - Technology choice decision record
- **[Dashboard Requirements](../docs/dashboard-requirements.md)** - Functional requirements

### Sprint Documentation

- **[Sprint F01: Mock API](../docs/tasklists/tasklist-F01.md)** - Mock API implementation
  - [Summary](../docs/tasklists/sprint-F01-summary.md)
- **[Sprint F02: Frontend Init](../docs/tasklists/tasklist-F02.md)** - Project structure setup
- **[Sprint F03: Dashboard](../docs/tasklists/tasklist-F03.md)** - Dashboard implementation
  - [Plan](./doc/plans/s3-dashboard-plan.md) - Detailed sprint plan
  - [Summary](../docs/tasklists/sprint-F03-summary.md) - Sprint summary
- **[Frontend Roadmap](../docs/frontend-roadmap.md)** - Full development roadmap

---

## 🎨 Components

### shadcn/ui Components

All UI components are based on [shadcn/ui](https://ui.shadcn.com/):
- Copy-pasted into the project (not npm package)
- Fully customizable
- Built on Radix UI primitives
- Accessible by default (WCAG AA)

**Installed components:**
- badge, button, card, chart, input, label, tabs

### Dashboard Components

**StatsCard** - Reusable metric card with trend indicators
```tsx
<StatsCard
  title="Active Users"
  value="1,234"
  change={12.5}
  trend="up"
  description="vs last month"
/>
```

**ActivityChart** - Area chart for time-series data
```tsx
<ActivityChart
  data={activityData}
  title="Activity"
  description="Last 30 days"
/>
```

**UserDistributionChart** - Bar + Pie charts
```tsx
<UserDistributionChart
  languageData={languages}
  premiumData={premium}
/>
```

**PeriodFilter** - Period selector tabs
```tsx
<PeriodFilter
  value={period}
  onChange={setPeriod}
/>
```

---

## 🔧 Configuration

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### TypeScript

**Strict mode enabled:**
```json
{
  "strict": true,
  "noUncheckedIndexedAccess": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true
}
```

### Tailwind CSS

**Custom theme variables:**
```css
/* Chart colors */
--chart-1: oklch(0.488 0.243 264.376)  /* Blue/Purple */
--chart-2: oklch(0.696 0.17 162.48)    /* Green */
--chart-3: oklch(0.769 0.188 70.08)    /* Yellow */
--chart-4: oklch(0.627 0.265 303.9)    /* Pink */
--chart-5: oklch(0.645 0.246 16.439)   /* Orange */
```

---

## 🧪 Testing

### Current Status

- ✅ TypeScript: 0 errors (strict mode)
- ✅ ESLint: 0 errors
- ✅ Manual testing: Dashboard fully functional

### Future Testing

- Unit tests: Vitest + React Testing Library
- E2E tests: Playwright
- Visual regression: Chromatic

---

## 🚧 Roadmap

### ✅ Completed

- [x] Sprint F01: Mock API for dashboard
- [x] Sprint F02: Frontend project structure
- [x] Sprint F03: Dashboard implementation

### 📋 Planned

- [ ] Sprint F04: AI Chat for admin (Text2SQL)
- [ ] Sprint F05: Transition to Real API

---

## 🔗 API Integration

### Mock API (Current)

**Endpoint:** `GET /api/stats/dashboard`

**Features:**
- Mock data generation
- Realistic statistics
- CORS enabled for development

**Start Mock API:**
```bash
cd ..
make api-dev
```

### Real API (Sprint F05)

**Planned features:**
- PostgreSQL integration
- JWT authentication
- Real-time statistics
- Time-series endpoints
- Rate limiting

---

## 📊 Performance

### Bundle Size

- **First Load JS:** ~120KB (gzipped)
- **recharts:** ~80KB
- **Next.js:** ~40KB

### Lighthouse Score

Target metrics:
- Performance: 90+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 100

---

## 🤝 Contributing

### Code Style

- Use TypeScript strict mode
- Follow ESLint rules
- Format with Prettier
- Write meaningful commit messages

### Component Guidelines

- Prefer Server Components by default
- Use Client Components only for interactivity
- Keep components small and focused
- Export types alongside components

### File Naming

- Components: `kebab-case.tsx`
- Types: `kebab-case.ts`
- Pages: `page.tsx` (Next.js convention)

---

## 📝 License

This project is part of the systech-aidd system.

---

## 🙏 Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for amazing UI components
- [Recharts](https://recharts.org/) for flexible charting library
- [Next.js](https://nextjs.org/) for the best React framework
- [Tailwind CSS](https://tailwindcss.com/) for utility-first styling

---

**Last Updated:** 2025-10-17 (Sprint F03 completed)  
**Version:** 1.0.0  
**Status:** Ready for production (with Mock API)
