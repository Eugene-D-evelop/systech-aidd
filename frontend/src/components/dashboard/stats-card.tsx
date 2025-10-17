import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { cn } from '@/lib/utils'
import { ArrowDownIcon, ArrowUpIcon } from 'lucide-react'

interface StatsCardProps {
    title: string
    value: string | number
    description?: string
    change?: number
    trend?: 'up' | 'down' | 'neutral'
    icon?: React.ReactNode
}

export function StatsCard({
    title,
    value,
    description,
    change,
    trend = 'neutral',
    icon,
}: StatsCardProps) {
    const showChange = change !== undefined && trend !== 'neutral'

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{title}</CardTitle>
                {icon}
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{value}</div>
                {(description || showChange) && (
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        {showChange && (
                            <span
                                className={cn(
                                    'flex items-center gap-0.5 font-medium',
                                    trend === 'up' && 'text-emerald-500',
                                    trend === 'down' && 'text-red-500'
                                )}
                            >
                                {trend === 'up' ? (
                                    <ArrowUpIcon className="h-3 w-3" />
                                ) : (
                                    <ArrowDownIcon className="h-3 w-3" />
                                )}
                                {Math.abs(change).toFixed(1)}%
                            </span>
                        )}
                        {description && <span>{description}</span>}
                    </div>
                )}
            </CardContent>
        </Card>
    )
}

