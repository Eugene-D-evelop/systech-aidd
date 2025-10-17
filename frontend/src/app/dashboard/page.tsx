import { FloatingChatButton } from '@/components/chat/floating-chat-button'
import { DashboardClient } from '@/components/dashboard/dashboard-client'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { getDashboardStats } from '@/lib/api'

export default async function DashboardPage() {
    let stats
    let error = null

    try {
        stats = await getDashboardStats()
    } catch (e) {
        error = e instanceof Error ? e.message : 'Failed to fetch stats'
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
                            Убедитесь, что Mock API запущен на localhost:8000
                        </p>
                        <code className="mt-2 block rounded bg-muted p-2 text-xs">
                            make api-dev
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
                <DashboardClient stats={stats!} />
            </div>

            {/* Floating chat button */}
            <FloatingChatButton />
        </>
    )
}

