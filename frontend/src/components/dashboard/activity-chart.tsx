'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ActivityDataPoint } from '@/lib/mock-time-series'
import {
    Area,
    AreaChart,
    CartesianGrid,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts'

interface ActivityChartProps {
    data: ActivityDataPoint[]
    title?: string
    description?: string
}

export function ActivityChart({
    data,
    title = 'Активность',
    description = 'Пользователи и сообщения по дням',
}: ActivityChartProps) {

    return (
        <Card>
            <CardHeader>
                <CardTitle>{title}</CardTitle>
                {description && (
                    <p className="text-sm text-muted-foreground">{description}</p>
                )}
            </CardHeader>
            <CardContent>
                <div className="h-[300px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart
                            data={data}
                            margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
                        >
                            <defs>
                                <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="hsl(var(--chart-1))" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="hsl(var(--chart-1))" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="colorMessages" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="hsl(var(--chart-2))" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="hsl(var(--chart-2))" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                            <XAxis
                                dataKey="date"
                                className="text-xs"
                                tick={{ fill: 'hsl(var(--muted-foreground))' }}
                            />
                            <YAxis
                                className="text-xs"
                                tick={{ fill: 'hsl(var(--muted-foreground))' }}
                            />
                            <Tooltip
                                content={({ active, payload }) => {
                                    if (!active || !payload || payload.length === 0) return null
                                    return (
                                        <div className="rounded-lg border bg-background p-2 shadow-md">
                                            <div className="text-sm font-medium">
                                                {payload[0]?.payload.date}
                                            </div>
                                            <div className="mt-1 space-y-1">
                                                {payload.map((entry, index) => (
                                                    <div
                                                        key={index}
                                                        className="flex items-center gap-2 text-xs"
                                                    >
                                                        <div
                                                            className="h-2 w-2 rounded-full"
                                                            style={{ backgroundColor: entry.color }}
                                                        />
                                                        <span className="text-muted-foreground">
                                                            {entry.name}:
                                                        </span>
                                                        <span className="font-medium">{entry.value}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )
                                }}
                            />
                            <Legend
                                wrapperStyle={{ paddingTop: '20px' }}
                                iconType="circle"
                            />
                            <Area
                                type="monotone"
                                dataKey="users"
                                name="Пользователи"
                                stroke="hsl(var(--chart-1))"
                                fill="url(#colorUsers)"
                                strokeWidth={2}
                            />
                            <Area
                                type="monotone"
                                dataKey="messages"
                                name="Сообщения"
                                stroke="hsl(var(--chart-2))"
                                fill="url(#colorMessages)"
                                strokeWidth={2}
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </CardContent>
        </Card>
    )
}

