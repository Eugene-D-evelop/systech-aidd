"""FastAPI приложение для предоставления статистики через REST API."""

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.stats.collector import StatCollector
from src.stats.mock_collector import MockStatCollector
from src.stats.models import DashboardStats

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

    В данной реализации используется MockStatCollector.
    В будущем (Sprint F05) можно будет переключаться на Real реализацию
    через конфигурацию.

    Returns:
        StatCollector: Экземпляр сборщика статистики
    """
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

