'use client'

import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'

export type Period = '7d' | '30d' | '90d'

interface PeriodFilterProps {
    value: Period
    onChange: (period: Period) => void
}

export function PeriodFilter({ value, onChange }: PeriodFilterProps) {
    return (
        <Tabs value={value} onValueChange={(v) => onChange(v as Period)}>
            <TabsList>
                <TabsTrigger value="7d">7 дней</TabsTrigger>
                <TabsTrigger value="30d">30 дней</TabsTrigger>
                <TabsTrigger value="90d">Всё время</TabsTrigger>
            </TabsList>
        </Tabs>
    )
}


