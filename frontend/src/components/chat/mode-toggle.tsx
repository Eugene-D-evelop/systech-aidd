import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import type { ChatMode } from '@/types/chat'

interface ModeToggleProps {
    mode: ChatMode
    onModeChange: (mode: ChatMode) => void
    disabled?: boolean
}

export function ModeToggle({
    mode,
    onModeChange,
    disabled = false,
}: ModeToggleProps) {
    return (
        <Tabs
            value={mode}
            onValueChange={(value) => onModeChange(value as ChatMode)}
        >
            <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="normal" disabled={disabled}>
                    💬 Обычный
                </TabsTrigger>
                <TabsTrigger value="admin" disabled={disabled}>
                    🔧 Админ
                </TabsTrigger>
            </TabsList>
        </Tabs>
    )
}

