const SESSION_ID_KEY = 'chat-session-id'

/**
 * Генерирует UUID v4
 */
function generateUUID(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(
        /[xy]/g,
        function (c) {
            const r = (Math.random() * 16) | 0
            const v = c === 'x' ? r : (r & 0x3) | 0x8
            return v.toString(16)
        }
    )
}

/**
 * Получить session ID из localStorage или создать новый
 */
export function getOrCreateSessionId(): string {
    if (typeof window === 'undefined') {
        // Server-side rendering
        return ''
    }

    try {
        const existing = localStorage.getItem(SESSION_ID_KEY)
        if (existing) {
            return existing
        }

        const newSessionId = generateUUID()
        localStorage.setItem(SESSION_ID_KEY, newSessionId)
        return newSessionId
    } catch (error) {
        console.error('Failed to access localStorage:', error)
        return generateUUID()
    }
}

/**
 * Получить текущий session ID (без создания нового)
 */
export function getSessionId(): string | null {
    if (typeof window === 'undefined') {
        return null
    }

    try {
        return localStorage.getItem(SESSION_ID_KEY)
    } catch (error) {
        console.error('Failed to access localStorage:', error)
        return null
    }
}

/**
 * Удалить session ID (для сброса сессии)
 */
export function clearSessionId(): void {
    if (typeof window === 'undefined') {
        return
    }

    try {
        localStorage.removeItem(SESSION_ID_KEY)
    } catch (error) {
        console.error('Failed to clear localStorage:', error)
    }
}

