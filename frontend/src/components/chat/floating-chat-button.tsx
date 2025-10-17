'use client'

import { Button } from '@/components/ui/button'
import { MessageCircle } from 'lucide-react'
import * as React from 'react'
import { ChatInterface } from './chat-interface'

export function FloatingChatButton() {
    const [isOpen, setIsOpen] = React.useState(false)

    return (
        <>
            {!isOpen && (
                <Button
                    onClick={() => setIsOpen(true)}
                    size="icon"
                    className="fixed bottom-4 right-4 z-50 size-14 rounded-full shadow-lg"
                >
                    <MessageCircle className="size-6" />
                    <span className="sr-only">Открыть чат</span>
                </Button>
            )}
            <ChatInterface isOpen={isOpen} onClose={() => setIsOpen(false)} />
        </>
    )
}

