import { Card, CardContent, CardHeader } from '@/components/ui/card'

function SkeletonCard() {
    return (
        <Card>
            <CardHeader className="space-y-0 pb-2">
                <div className="h-4 w-24 animate-pulse rounded bg-muted" />
            </CardHeader>
            <CardContent>
                <div className="h-8 w-32 animate-pulse rounded bg-muted" />
                <div className="mt-2 h-3 w-40 animate-pulse rounded bg-muted" />
            </CardContent>
        </Card>
    )
}

function SkeletonChart() {
    return (
        <Card>
            <CardHeader>
                <div className="h-6 w-48 animate-pulse rounded bg-muted" />
                <div className="mt-2 h-4 w-64 animate-pulse rounded bg-muted" />
            </CardHeader>
            <CardContent>
                <div className="h-[300px] animate-pulse rounded bg-muted" />
            </CardContent>
        </Card>
    )
}

export default function DashboardLoading() {
    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="space-y-2">
                    <div className="h-9 w-48 animate-pulse rounded bg-muted" />
                    <div className="h-5 w-64 animate-pulse rounded bg-muted" />
                </div>
                <div className="h-6 w-24 animate-pulse rounded-full bg-muted" />
            </div>

            {/* Stats Cards Grid - First Row */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <SkeletonCard />
                <SkeletonCard />
                <SkeletonCard />
                <SkeletonCard />
            </div>

            {/* Stats Cards Grid - Second Row */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <SkeletonCard />
                <SkeletonCard />
                <SkeletonCard />
            </div>

            {/* Activity Chart Section */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <div className="h-7 w-48 animate-pulse rounded bg-muted" />
                    <div className="h-10 w-80 animate-pulse rounded-md bg-muted" />
                </div>
                <SkeletonChart />
            </div>

            {/* Distribution Charts */}
            <div className="space-y-4">
                <div className="h-7 w-56 animate-pulse rounded bg-muted" />
                <div className="grid gap-6 lg:grid-cols-2">
                    <SkeletonChart />
                    <SkeletonChart />
                </div>
            </div>
        </div>
    )
}

