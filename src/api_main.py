"""Entrypoint для запуска API сервера статистики."""

import os

import uvicorn


def main() -> None:
    """Запуск API сервера с конфигурацией из переменных окружения."""
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"

    uvicorn.run(
        "src.api.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()

