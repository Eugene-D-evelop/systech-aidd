'use client'

import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { getChatHistory, sendChatMessage } from '@/lib/chat-api'
import { getOrCreateSessionId } from '@/lib/chat-storage'
import { cn } from '@/lib/utils'
import type { ChatMode, Message } from '@/types/chat'
import { X } from 'lucide-react'
import * as React from 'react'
import { ChatInput } from './chat-input'
import { ChatMessage } from './chat-message'
import { ModeToggle } from './mode-toggle'

interface ChatInterfaceProps {
    isOpen: boolean
    onClose: () => void
}

export function ChatInterface({ isOpen, onClose }: ChatInterfaceProps) {
    const [messages, setMessages] = React.useState<Message[]>([])
    const [isLoading, setIsLoading] = React.useState(false)
    const [mode, setMode] = React.useState<ChatMode>('normal')
    const [sessionId, setSessionId] = React.useState('')
    const scrollRef = React.useRef<HTMLDivElement>(null)

    // Initialize session and load history
    React.useEffect(() => {
        if (isOpen && !sessionId) {
            const id = getOrCreateSessionId()
            setSessionId(id)
            loadHistory(id)
        }
    }, [isOpen, sessionId])

    // Auto-scroll to bottom when new messages arrive
    React.useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight
        }
    }, [messages])

    const loadHistory = async (sid: string) => {
        try {
            const history = await getChatHistory(sid, 50)
            const loadedMessages: Message[] = history.messages.map(
                (msg, idx) => ({
                    id: `${sid}-${idx}`,
                    role: msg.role,
                    content: msg.content,
                    timestamp: new Date(),
                    sqlQuery: msg.sql_query || undefined,
                })
            )
            setMessages(loadedMessages)
        } catch (error) {
            console.error('Failed to load history:', error)
        }
    }

    const handleSend = async (message: string) => {
        if (!sessionId || !message.trim()) return

        // Add user message immediately
        const userMessage: Message = {
            id: `${sessionId}-${Date.now()}-user`,
            role: 'user',
            content: message,
            timestamp: new Date(),
        }
        setMessages((prev) => [...prev, userMessage])
        setIsLoading(true)

        try {
            const response = await sendChatMessage(message, sessionId, mode)

            // Add assistant response
            const assistantMessage: Message = {
                id: `${sessionId}-${Date.now()}-assistant`,
                role: 'assistant',
                content: response.response,
                timestamp: new Date(),
                sqlQuery: response.sql_query || undefined,
            }
            setMessages((prev) => [...prev, assistantMessage])
        } catch (error) {
            console.error('Failed to send message:', error)
            // Add error message
            const errorMessage: Message = {
                id: `${sessionId}-${Date.now()}-error`,
                role: 'assistant',
                content: `Ошибка: ${error instanceof Error ? error.message : 'Не удалось отправить сообщение'}`,
                timestamp: new Date(),
            }
            setMessages((prev) => [...prev, errorMessage])
        } finally {
            setIsLoading(false)
        }
    }

    if (!isOpen) return null

    return (
        <div
            className={cn(
                'fixed bottom-4 right-4 z-50',
                'w-96 h-[600px]',
                'max-md:inset-0 max-md:w-full max-md:h-full max-md:bottom-0 max-md:right-0',
                'bg-background border rounded-lg shadow-2xl',
                'flex flex-col'
            )}
        >
            {/* Header */}
            <div className="flex items-center justify-between border-b p-4">
                <div className="space-y-1">
                    <h2 className="text-lg font-semibold">AI Ассистент</h2>
                    <p className="text-xs text-muted-foreground">
                        {mode === 'admin'
                            ? 'Режим администратора (Text2Postgre)'
                            : 'Обычный режим'}
                    </p>
                </div>
                <Button
                    variant="ghost"
                    size="icon"
                    onClick={onClose}
                    className="shrink-0"
                >
                    <X className="size-4" />
                    <span className="sr-only">Закрыть</span>
                </Button>
            </div>

            {/* Mode Toggle */}
            <div className="border-b p-4">
                <ModeToggle
                    mode={mode}
                    onModeChange={setMode}
                    disabled={isLoading}
                />
            </div>

            {/* Messages */}
            <ScrollArea className="flex-1 p-4">
                <div ref={scrollRef} className="flex flex-col gap-4">
                    {messages.length === 0 && (
                        <div className="flex items-center justify-center h-full text-center text-muted-foreground">
                            <p>
                                Начните диалог с AI-ассистентом.
                                <br />
                                {mode === 'admin' && (
                                    <span className="text-xs">
                                        В режиме администратора вы можете
                                        задавать вопросы по статистике бота.
                                    </span>
                                )}
                            </p>
                        </div>
                    )}
                    {messages.map((msg) => (
                        <ChatMessage key={msg.id} message={msg} />
                    ))}
                    {isLoading && (
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <div className="size-4 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                            <span>AI думает...</span>
                        </div>
                    )}
                </div>
            </ScrollArea>

            {/* Input */}
            <div className="border-t p-4">
                <ChatInput
                    onSend={handleSend}
                    disabled={isLoading}
                    placeholder={
                        mode === 'admin'
                            ? 'Спросите о статистике...'
                            : 'Введите сообщение...'
                    }
                />
            </div>
        </div>
    )
}

