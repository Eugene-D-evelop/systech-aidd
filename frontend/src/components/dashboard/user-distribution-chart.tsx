'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
    Bar,
    BarChart,
    Cell,
    Legend,
    Pie,
    PieChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts'

interface LanguageData {
    language: string
    count: number
    label: string
}

interface PremiumData {
    name: string
    value: number
    percentage: number
    [key: string]: string | number // Index signature for recharts
}

interface UserDistributionChartProps {
    languageData: LanguageData[]
    premiumData: PremiumData[]
}

const LANGUAGE_COLORS = [
    'hsl(var(--chart-1))',
    'hsl(var(--chart-2))',
    'hsl(var(--chart-3))',
    'hsl(var(--chart-4))',
]

const PREMIUM_COLORS = {
    Premium: 'hsl(var(--chart-3))', // Yellow/gold for premium
    Regular: 'hsl(var(--muted))', // Gray for regular
}

export function UserDistributionChart({
    languageData,
    premiumData,
}: UserDistributionChartProps) {
    return (
        <div className="grid gap-6 lg:grid-cols-2">
            {/* Language Distribution - Bar Chart */}
            <Card>
                <CardHeader>
                    <CardTitle>Языки пользователей</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart
                                data={languageData}
                                layout="vertical"
                                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                            >
                                <XAxis
                                    type="number"
                                    className="text-xs"
                                    tick={{ fill: 'hsl(var(--muted-foreground))' }}
                                />
                                <YAxis
                                    type="category"
                                    dataKey="label"
                                    className="text-xs"
                                    tick={{ fill: 'hsl(var(--muted-foreground))' }}
                                    width={80}
                                />
                                <Tooltip
                                    content={({ active, payload }) => {
                                        if (!active || !payload || payload.length === 0)
                                            return null
                                        const data = payload[0]?.payload
                                        return (
                                            <div className="rounded-lg border bg-background p-2 shadow-md">
                                                <div className="text-sm font-medium">{data.label}</div>
                                                <div className="text-xs text-muted-foreground">
                                                    {data.count} пользователей
                                                </div>
                                            </div>
                                        )
                                    }}
                                />
                                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                                    {languageData.map((_entry, index) => (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={LANGUAGE_COLORS[index % LANGUAGE_COLORS.length]}
                                        />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </CardContent>
            </Card>

            {/* Premium Distribution - Pie Chart */}
            <Card>
                <CardHeader>
                    <CardTitle>Premium пользователи</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={premiumData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={100}
                                    paddingAngle={2}
                                    dataKey="value"
                                >
                                    {premiumData.map((entry, index) => (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={
                                                PREMIUM_COLORS[entry.name as keyof typeof PREMIUM_COLORS]
                                            }
                                        />
                                    ))}
                                </Pie>
                                <Tooltip
                                    content={({ active, payload }) => {
                                        if (!active || !payload || payload.length === 0)
                                            return null
                                        const data = payload[0]?.payload
                                        return (
                                            <div className="rounded-lg border bg-background p-2 shadow-md">
                                                <div className="text-sm font-medium">{data.name}</div>
                                                <div className="text-xs text-muted-foreground">
                                                    {data.value} ({data.percentage.toFixed(1)}%)
                                                </div>
                                            </div>
                                        )
                                    }}
                                />
                                <Legend
                                    verticalAlign="bottom"
                                    height={36}
                                    formatter={(value, entry) => {
                                        const data = entry.payload as unknown as PremiumData
                                        return `${value}: ${data.percentage.toFixed(1)}%`
                                    }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

