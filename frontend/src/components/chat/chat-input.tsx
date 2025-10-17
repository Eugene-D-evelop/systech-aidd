import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { cn } from '@/lib/utils'
import { CornerDownLeft } from 'lucide-react'
import * as React from 'react'

interface ChatInputProps {
    onSend: (message: string) => void
    disabled?: boolean
    placeholder?: string
}

export function ChatInput({
    onSend,
    disabled = false,
    placeholder = 'Введите сообщение...',
}: ChatInputProps) {
    const [value, setValue] = React.useState('')

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (value.trim() && !disabled) {
            onSend(value.trim())
            setValue('')
        }
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit(e)
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="relative rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring p-1"
        >
            <Textarea
                value={value}
                onChange={(e) => setValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                disabled={disabled}
                className={cn(
                    'min-h-12 resize-none rounded-lg bg-background border-0 p-3 shadow-none focus-visible:ring-0',
                    'max-h-32'
                )}
            />
            <div className="flex items-center p-3 pt-0">
                <Button
                    type="submit"
                    size="sm"
                    className="ml-auto gap-1.5"
                    disabled={disabled || !value.trim()}
                >
                    Отправить
                    <CornerDownLeft className="size-3.5" />
                </Button>
            </div>
        </form>
    )
}

