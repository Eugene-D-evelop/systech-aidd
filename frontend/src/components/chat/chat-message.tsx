import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import type { Message } from '@/types/chat'

interface ChatMessageProps {
    message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
    const isUser = message.role === 'user'

    return (
        <div
            className={cn(
                'flex w-full gap-3 text-sm',
                isUser ? 'justify-end' : 'justify-start'
            )}
        >
            {!isUser && (
                <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
                    AI
                </div>
            )}
            <div
                className={cn(
                    'flex flex-col gap-2 rounded-lg px-4 py-3 max-w-[80%]',
                    isUser
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                )}
            >
                <div className="whitespace-pre-wrap break-words">
                    {message.content}
                </div>
                {message.sqlQuery && (
                    <div className="space-y-1">
                        <Badge variant="outline" className="text-xs">
                            SQL Query
                        </Badge>
                        <pre className="text-xs bg-background/50 rounded p-2 overflow-x-auto">
                            {message.sqlQuery}
                        </pre>
                    </div>
                )}
            </div>
            {isUser && (
                <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-muted">
                    👤
                </div>
            )}
        </div>
    )
}

