'use client'

import type { ActivityDataPoint } from '@/lib/mock-time-series'
import {
    calculateActivityChange,
    generateActivityData,
    generateLanguageData,
    generatePremiumData,
    getTrend,
} from '@/lib/mock-time-series'
import type { DashboardStats } from '@/types/stats'
import { BarChart3, Clock, MessageSquare, Users } from 'lucide-react'
import { useEffect, useState } from 'react'
import { ActivityChart } from './activity-chart'
import { PeriodFilter, type Period } from './period-filter'
import { StatsCard } from './stats-card'
import { UserDistributionChart } from './user-distribution-chart'

interface DashboardClientProps {
    stats: DashboardStats
}

export function DashboardClient({ stats }: DashboardClientProps) {
    const [period, setPeriod] = useState<Period>('30d')
    const [activityData, setActivityData] = useState<ActivityDataPoint[]>([])
    const [mounted, setMounted] = useState(false)

    // Generate activity data only on client side to avoid hydration mismatch
    useEffect(() => {
        setActivityData(generateActivityData(period))
        setMounted(true)
    }, [period])

    // Generate distribution data (stable, no random)
    const languageData = generateLanguageData(stats.users.by_language)
    const premiumData = generatePremiumData(
        stats.users.premium_count,
        stats.users.regular_count,
        stats.users.premium_percentage
    )

    // Calculate changes for stats cards
    const usersChange = calculateActivityChange(
        stats.overview.active_users_7d,
        stats.overview.active_users_30d
    )
    const messagesChange = calculateActivityChange(
        stats.overview.messages_7d,
        stats.overview.messages_30d
    )

    return (
        <>
            {/* Stats Cards Grid */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <StatsCard
                    title="Всего пользователей"
                    value={stats.overview.total_users.toLocaleString('en-US')}
                    description="Зарегистрировано в боте"
                    icon={<Users className="h-4 w-4 text-muted-foreground" />}
                />
                <StatsCard
                    title="Активные (7д)"
                    value={stats.overview.active_users_7d.toLocaleString('en-US')}
                    description="vs прошлый месяц"
                    change={usersChange}
                    trend={getTrend(usersChange)}
                    icon={<Users className="h-4 w-4 text-muted-foreground" />}
                />
                <StatsCard
                    title="Всего сообщений"
                    value={stats.overview.total_messages.toLocaleString('en-US')}
                    description="Обработано ботом"
                    icon={<MessageSquare className="h-4 w-4 text-muted-foreground" />}
                />
                <StatsCard
                    title="Сообщений (7д)"
                    value={stats.overview.messages_7d.toLocaleString('en-US')}
                    description="vs прошлый месяц"
                    change={messagesChange}
                    trend={getTrend(messagesChange)}
                    icon={<MessageSquare className="h-4 w-4 text-muted-foreground" />}
                />
            </div>

            {/* Additional Stats Row */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <StatsCard
                    title="Средняя длина"
                    value={`${stats.messages.avg_length.toFixed(0)} символов`}
                    description="Длина сообщения пользователя"
                    icon={<BarChart3 className="h-4 w-4 text-muted-foreground" />}
                />
                <StatsCard
                    title="Premium пользователи"
                    value={`${stats.users.premium_percentage.toFixed(1)}%`}
                    description={`${stats.users.premium_count} из ${stats.overview.total_users}`}
                    icon={<Users className="h-4 w-4 text-muted-foreground" />}
                />
                <StatsCard
                    title="Соотношение"
                    value={stats.messages.user_to_assistant_ratio.toFixed(2)}
                    description="Сообщений пользователь/бот"
                    icon={<Clock className="h-4 w-4 text-muted-foreground" />}
                />
            </div>

            {/* Period Filter and Activity Chart */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold">График активности</h2>
                    <PeriodFilter value={period} onChange={setPeriod} />
                </div>
                {mounted && activityData.length > 0 ? (
                    <ActivityChart
                        data={activityData}
                        title="Пользователи и сообщения"
                        description={
                            period === '7d'
                                ? 'За последние 7 дней'
                                : period === '30d'
                                    ? 'За последние 30 дней'
                                    : 'За последние 3 месяца'
                        }
                    />
                ) : (
                    <div className="h-[400px] animate-pulse rounded-lg bg-muted" />
                )}
            </div>

            {/* User Distribution Charts */}
            <div className="space-y-4">
                <h2 className="text-xl font-semibold">Распределение пользователей</h2>
                <UserDistributionChart
                    languageData={languageData}
                    premiumData={premiumData}
                />
            </div>
        </>
    )
}

