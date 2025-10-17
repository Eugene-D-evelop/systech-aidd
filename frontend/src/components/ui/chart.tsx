"use client"

import * as React from "react"
import * as RechartsPrimitive from "recharts"

import { cn } from "@/lib/utils"

// Chart component wrapping recharts with theme support
const ChartContainer = React.forwardRef<
    HTMLDivElement,
    React.ComponentProps<"div"> & {
        config?: Record<string, { label: string; theme?: Record<string, string> }>
        children: React.ComponentProps<
            typeof RechartsPrimitive.ResponsiveContainer
        >["children"]
    }
>(({ className, children, ...props }, ref) => {
    return (
        <div
            ref={ref}
            className={cn("flex aspect-video justify-center text-xs", className)}
            {...props}
        >
            <RechartsPrimitive.ResponsiveContainer width="100%" height="100%">
                {children}
            </RechartsPrimitive.ResponsiveContainer>
        </div>
    )
})
ChartContainer.displayName = "ChartContainer"

const ChartTooltip = RechartsPrimitive.Tooltip

const ChartTooltipContent = React.forwardRef<
    HTMLDivElement,
    React.ComponentProps<"div">
>(({ className, ...props }, ref) => {
    return (
        <div
            ref={ref}
            className={cn(
                "grid min-w-[8rem] gap-1.5 rounded-lg border bg-background p-2.5 text-xs shadow-xl",
                className
            )}
            {...props}
        />
    )
}
)
ChartTooltipContent.displayName = "ChartTooltipContent"

const ChartLegend = RechartsPrimitive.Legend

const ChartLegendContent = React.forwardRef<
    HTMLDivElement,
    React.ComponentProps<"div">
>(({ className, ...props }, ref) => {
    return (
        <div
            ref={ref}
            className={cn("flex items-center justify-center gap-4", className)}
            {...props}
        />
    )
})
ChartLegendContent.displayName = "ChartLegendContent"

export {
    ChartContainer, ChartLegend,
    ChartLegendContent, ChartTooltip,
    ChartTooltipContent
}

