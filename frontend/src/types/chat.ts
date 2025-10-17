export type ChatMode = 'normal' | 'admin'

export type MessageRole = 'user' | 'assistant' | 'system'

export interface Message {
    id: string
    role: MessageRole
    content: string
    timestamp: Date
    sqlQuery?: string // Only for admin mode responses
}

export interface ChatState {
    messages: Message[]
    isOpen: boolean
    isLoading: boolean
    sessionId: string
    mode: ChatMode
}

export interface ChatMessageRequest {
    message: string
    session_id: string
    mode: ChatMode
}

export interface ChatMessageResponse {
    response: string
    session_id: string
    sql_query: string | null
}

export interface ChatHistoryMessage {
    role: MessageRole
    content: string
    sql_query: string | null
}

export interface ChatHistoryResponse {
    messages: ChatHistoryMessage[]
    session_id: string
}

