import { format, subDays } from 'date-fns'

export interface ActivityDataPoint {
    date: string
    users: number
    messages: number
}

type Period = '7d' | '30d' | '90d'

/**
 * Генерирует mock time-series данные для Activity Chart
 * В Sprint F05 эти данные будут приходить из реального API
 */
export function generateActivityData(period: Period): ActivityDataPoint[] {
    const days = period === '7d' ? 7 : period === '30d' ? 30 : 90
    const data: ActivityDataPoint[] = []
    const today = new Date()

    // Базовые значения для генерации реалистичных данных
    const baseUsers = 120
    const baseMessages = 450

    for (let i = days - 1; i >= 0; i--) {
        const date = subDays(today, i)

        // Добавляем случайную вариацию и тренд
        const dayOfWeek = date.getDay()
        const weekendMultiplier = dayOfWeek === 0 || dayOfWeek === 6 ? 0.7 : 1.0

        // Случайные колебания ±20%
        const randomVariation = 0.8 + Math.random() * 0.4

        // Небольшой восходящий тренд
        const trendMultiplier = 1 + (days - i) / (days * 10)

        const users = Math.round(
            baseUsers * weekendMultiplier * randomVariation * trendMultiplier
        )

        const messages = Math.round(
            baseMessages * weekendMultiplier * randomVariation * trendMultiplier
        )

        data.push({
            date: format(date, period === '7d' ? 'EEE' : 'MMM d'),
            users,
            messages,
        })
    }

    return data
}

/**
 * Генерирует данные для Language Distribution Bar Chart
 */
export function generateLanguageData(
    byLanguage: Record<string, number>
): Array<{ language: string; count: number; label: string }> {
    const languageLabels: Record<string, string> = {
        ru: 'Русский',
        en: 'English',
        de: 'Deutsch',
        other: 'Другие',
    }

    return Object.entries(byLanguage)
        .map(([language, count]) => ({
            language,
            count,
            label: languageLabels[language] || language.toUpperCase(),
        }))
        .sort((a, b) => b.count - a.count)
}

/**
 * Генерирует данные для Premium Distribution Pie Chart
 */
export function generatePremiumData(
    premiumCount: number,
    regularCount: number,
    premiumPercentage: number
): Array<{ name: string; value: number; percentage: number }> {
    return [
        {
            name: 'Premium',
            value: premiumCount,
            percentage: premiumPercentage,
        },
        {
            name: 'Regular',
            value: regularCount,
            percentage: 100 - premiumPercentage,
        },
    ]
}

/**
 * Вычисляет процент изменения между двумя значениями
 */
export function calculateChange(current: number, previous: number): number {
    if (previous === 0) return 0
    return ((current - previous) / previous) * 100
}

/**
 * Вычисляет изменение активности на основе данных за 7d и 30d
 * Экстраполирует 7d данные на 30 дней и сравнивает
 */
export function calculateActivityChange(
    value7d: number,
    value30d: number
): number {
    // Экстраполируем 7d на 30 дней
    const extrapolated30d = (value7d * 30) / 7
    return calculateChange(extrapolated30d, value30d)
}

/**
 * Форматирует процент изменения для отображения
 */
export function formatChange(change: number): string {
    const sign = change > 0 ? '+' : ''
    return `${sign}${change.toFixed(1)}%`
}

/**
 * Определяет тренд на основе процента изменения
 */
export function getTrend(change: number): 'up' | 'down' | 'neutral' {
    if (Math.abs(change) < 0.5) return 'neutral'
    return change > 0 ? 'up' : 'down'
}

