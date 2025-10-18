import type { DashboardStats } from '@/types/stats'

// Для server-side запросов используем API_URL (внутренний Docker network)
// Для client-side запросов используем NEXT_PUBLIC_API_URL (localhost для браузера)
const getApiUrl = () => {
    // Если код выполняется на сервере (SSR) и установлен API_URL
    if (typeof window === 'undefined' && process.env.API_URL) {
        return process.env.API_URL
    }
    // Для client-side или если API_URL не установлен
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
}

export async function getDashboardStats(): Promise<DashboardStats> {
    const apiUrl = getApiUrl()
    const response = await fetch(`${apiUrl}/api/stats/dashboard`, {
        cache: 'no-store', // Always fetch fresh data
    })

    if (!response.ok) {
        throw new Error(`Failed to fetch dashboard stats: ${response.statusText}`)
    }

    return response.json()
}

