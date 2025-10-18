import type {
    ChatHistoryResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    ChatMode,
} from '@/types/chat'

// Для server-side запросов используем API_URL (внутренний Docker network)
// Для client-side запросов используем NEXT_PUBLIC_API_URL (localhost для браузера)
const getApiUrl = () => {
    // Если код выполняется на сервере (SSR) и установлен API_URL
    if (typeof window === 'undefined' && process.env.API_URL) {
        return process.env.API_URL
    }
    // Для client-side или если API_URL не установлен
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
}

const API_URL = getApiUrl()

export async function sendChatMessage(
    message: string,
    sessionId: string,
    mode: ChatMode = 'normal'
): Promise<ChatMessageResponse> {
    const request: ChatMessageRequest = {
        message,
        session_id: sessionId,
        mode,
    }

    const response = await fetch(`${API_URL}/api/chat/message`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
    })

    if (!response.ok) {
        const error = await response.text()
        throw new Error(`Failed to send message: ${error}`)
    }

    return response.json()
}

export async function getChatHistory(
    sessionId: string,
    limit: number = 50
): Promise<ChatHistoryResponse> {
    const response = await fetch(
        `${API_URL}/api/chat/history/${sessionId}?limit=${limit}`,
        {
            method: 'GET',
        }
    )

    if (!response.ok) {
        const error = await response.text()
        throw new Error(`Failed to fetch history: ${error}`)
    }

    return response.json()
}

export async function clearChatHistory(sessionId: string): Promise<void> {
    const response = await fetch(`${API_URL}/api/chat/history/${sessionId}`, {
        method: 'DELETE',
    })

    if (!response.ok) {
        const error = await response.text()
        throw new Error(`Failed to clear history: ${error}`)
    }
}

