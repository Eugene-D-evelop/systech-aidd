import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
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
                        <CardTitle>Error</CardTitle>
                        <CardDescription>Failed to load dashboard statistics</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-muted-foreground">{error}</p>
                        <p className="mt-2 text-sm">
                            Make sure the Mock API is running on localhost:8000
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
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <p className="text-muted-foreground">
                    AI Bot Statistics {stats?.metadata.is_mock && '(Mock Data)'}
                </p>
            </div>

            {/* Overview Stats */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card>
                    <CardHeader className="pb-2">
                        <CardDescription>Total Users</CardDescription>
                        <CardTitle className="text-3xl">
                            {stats?.overview.total_users}
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-xs text-muted-foreground">
                            Active 7d: {stats?.overview.active_users_7d} | 30d:{' '}
                            {stats?.overview.active_users_30d}
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="pb-2">
                        <CardDescription>Total Messages</CardDescription>
                        <CardTitle className="text-3xl">
                            {stats?.overview.total_messages}
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-xs text-muted-foreground">
                            7d: {stats?.overview.messages_7d} | 30d:{' '}
                            {stats?.overview.messages_30d}
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="pb-2">
                        <CardDescription>Avg Message Length</CardDescription>
                        <CardTitle className="text-3xl">
                            {stats?.messages.avg_length.toFixed(0)}
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-xs text-muted-foreground">characters</p>
                    </CardContent>
                </Card>
            </div>

            {/* User Stats */}
            <Card>
                <CardHeader>
                    <CardTitle>User Distribution</CardTitle>
                    <CardDescription>Premium vs Regular users</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2">
                        <div className="flex justify-between">
                            <span className="text-sm">Premium Users</span>
                            <span className="text-sm font-medium">
                                {stats?.users.premium_count} ({stats?.users.premium_percentage.toFixed(1)}%)
                            </span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-sm">Regular Users</span>
                            <span className="text-sm font-medium">
                                {stats?.users.regular_count}
                            </span>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Message Stats */}
            <Card>
                <CardHeader>
                    <CardTitle>Message Statistics</CardTitle>
                    <CardDescription>Timeline and ratios</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                            <span>First Message</span>
                            <span className="font-medium">
                                {new Date(stats?.messages.first_message_date || '').toLocaleDateString()}
                            </span>
                        </div>
                        <div className="flex justify-between">
                            <span>Last Message</span>
                            <span className="font-medium">
                                {new Date(stats?.messages.last_message_date || '').toLocaleDateString()}
                            </span>
                        </div>
                        <div className="flex justify-between">
                            <span>User to Assistant Ratio</span>
                            <span className="font-medium">
                                {stats?.messages.user_to_assistant_ratio.toFixed(2)}
                            </span>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

