'use client'

import { FloatingChatButton } from '@/components/chat/floating-chat-button'
import { DashboardClient } from '@/components/dashboard/dashboard-client'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { getDashboardStats } from '@/lib/api'
import type { DashboardStats } from '@/types/stats'
import { useEffect, useState } from 'react'

export default function DashboardPage() {
    const [stats, setStats] = useState<DashboardStats | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchStats() {
            try {
                const data = await getDashboardStats()
                setStats(data)
                setError(null)
            } catch (e) {
                setError(e instanceof Error ? e.message : 'Failed to fetch stats')
            } finally {
                setLoading(false)
            }
        }

        fetchStats()
    }, [])

    if (loading) {
        return (
            <div className="space-y-4">
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-center py-8">
                            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
                        </div>
                        <p className="text-center text-sm text-muted-foreground">
                            Загрузка данных...
                        </p>
                    </CardContent>
                </Card>
            </div>
        )
    }

    if (error) {
        return (
            <div className="space-y-4">
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <Card>
                    <CardHeader>
                        <CardTitle>Ошибка загрузки данных</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-muted-foreground">{error}</p>
                        <p className="mt-2 text-sm">
                            Убедитесь, что API доступен
                        </p>
                        <code className="mt-2 block rounded bg-muted p-2 text-xs">
                            API: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
                        </code>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <>
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold">Dashboard</h1>
                        <p className="text-muted-foreground">
                            Статистика AI-бота для Telegram
                        </p>
                    </div>
                    {stats?.metadata.is_mock && (
                        <Badge variant="secondary">Mock Data</Badge>
                    )}
                </div>

                {/* Client component handles all interactivity */}
                {stats && <DashboardClient stats={stats} />}
            </div>

            {/* Floating chat button */}
            <FloatingChatButton />
        </>
    )
}

