import Link from 'next/link'

export function Header() {
    return (
        <header className="border-b">
            <div className="container mx-auto flex h-16 items-center px-4">
                <Link href="/" className="text-xl font-bold">
                    systech-aidd
                </Link>
                <nav className="ml-auto flex gap-6">
                    <Link
                        href="/dashboard"
                        className="text-sm font-medium transition-colors hover:text-primary"
                    >
                        Dashboard
                    </Link>
                    <span className="text-sm font-medium text-muted-foreground">
                        AI Chat (Coming Soon)
                    </span>
                </nav>
            </div>
        </header>
    )
}

