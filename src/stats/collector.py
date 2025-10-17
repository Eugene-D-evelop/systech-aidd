"""Абстрактный интерфейс для сборщиков статистики."""

from abc import ABC, abstractmethod

from src.stats.models import DashboardStats


class StatCollector(ABC):
    """Абстрактный базовый класс для сборщиков статистики.

    Позволяет легко переключаться между Mock и Real реализациями.
    """

    @abstractmethod
    async def get_dashboard_stats(self) -> DashboardStats:
        """Получение статистики для дашборда.

        Returns:
            DashboardStats: Полная статистика для дашборда
        """
        pass

