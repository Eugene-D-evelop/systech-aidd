"""FastAPI приложение для предоставления статистики через REST API."""

import os
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Database
from src.stats.collector import StatCollector
from src.stats.mock_collector import MockStatCollector
from src.stats.models import DashboardStats
from src.stats.real_collector import RealStatCollector

# Создание FastAPI приложения
app = FastAPI(
    title="Systech AIDD Statistics API",
    description="API для получения статистики использования AI-бота",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Настройка CORS для интеграции с frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production следует ограничить конкретными доменами
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency injection для StatCollector
def get_stat_collector() -> StatCollector:
    """Создание экземпляра сборщика статистики.

    Переключение между Mock и Real реализацией через переменную окружения:
    - USE_REAL_STATS=true - использовать реальные данные из БД
    - USE_REAL_STATS=false или не установлена - использовать Mock данные

    Returns:
        StatCollector: Экземпляр сборщика статистики (Mock или Real)
    """
    use_real_stats = os.getenv("USE_REAL_STATS", "false").lower() == "true"

    if use_real_stats:
        # Используем реальные данные из PostgreSQL
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/systech_aidd"
        )
        database_timeout = int(os.getenv("DATABASE_TIMEOUT", "10"))
        database = Database(database_url, database_timeout)
        return RealStatCollector(database)
    # Используем Mock данные (по умолчанию)
    return MockStatCollector()


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Корневой endpoint для проверки работоспособности API.

    Returns:
        dict: Информация о статусе API
    """
    return {
        "status": "ok",
        "message": "Systech AIDD Statistics API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/api/stats/dashboard", response_model=DashboardStats, tags=["Statistics"])
async def get_dashboard_stats(
    collector: Annotated[StatCollector, Depends(get_stat_collector)],
) -> DashboardStats:
    """Получение статистики для дашборда.

    Args:
        collector: Сборщик статистики (dependency injection)

    Returns:
        DashboardStats: Полная статистика для дашборда
    """
    return await collector.get_dashboard_stats()


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint для мониторинга.

    Returns:
        dict: Статус здоровья сервиса
    """
    return {"status": "healthy"}
