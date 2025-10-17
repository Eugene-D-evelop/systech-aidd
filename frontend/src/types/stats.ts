// TypeScript types for Mock API responses (from Sprint F01)
// Based on Pydantic models from backend

export interface OverviewStats {
    total_users: number
    active_users_7d: number
    active_users_30d: number
    total_messages: number
    messages_7d: number
    messages_30d: number
}

export interface UserStats {
    premium_count: number
    premium_percentage: number
    regular_count: number
    by_language: {
        [key: string]: number
    }
}

export interface MessageStats {
    avg_length: number
    first_message_date: string
    last_message_date: string
    user_to_assistant_ratio: number
}

export interface MetadataStats {
    generated_at: string
    is_mock: boolean
}

export interface DashboardStats {
    overview: OverviewStats
    users: UserStats
    messages: MessageStats
    metadata: MetadataStats
}

