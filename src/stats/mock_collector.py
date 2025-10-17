"""Mock реализация сборщика статистики для тестирования и разработки frontend."""

import random
from datetime import datetime, timedelta

from src.stats.collector import StatCollector
from src.stats.models import (
    DashboardStats,
    MessageStats,
    MetadataStats,
    OverviewStats,
    UserStats,
)


class MockStatCollector(StatCollector):
    """Mock реализация StatCollector с генерацией реалистичных тестовых данных."""

    async def get_dashboard_stats(self) -> DashboardStats:
        """Генерация Mock статистики для дашборда.

        Генерирует реалистичные данные с соблюдением логических связей.

        Returns:
            DashboardStats: Mock статистика для дашборда
        """
        # Генерация базовых метрик
        total_users = random.randint(100, 500)
        active_users_30d = int(total_users * random.uniform(0.5, 0.7))
        active_users_7d = int(active_users_30d * random.uniform(0.3, 0.6))

        total_messages = int(total_users * random.uniform(10, 30))
        messages_30d = int(total_messages * random.uniform(0.4, 0.6))
        messages_7d = int(messages_30d * random.uniform(0.3, 0.45))

        # Генерация данных о пользователях
        premium_count = int(total_users * random.uniform(0.1, 0.2))
        regular_count = total_users - premium_count
        premium_percentage = round((premium_count / total_users) * 100, 2)

        # Распределение по языкам
        ru_count = int(total_users * random.uniform(0.55, 0.7))
        en_count = int(total_users * random.uniform(0.2, 0.35))
        uk_count = int(total_users * random.uniform(0.03, 0.08))
        other_count = total_users - (ru_count + en_count + uk_count)

        # Корректировка для точного соответствия
        if other_count < 0:
            ru_count += other_count
            other_count = 0

        # Генерация данных о сообщениях
        avg_length = round(random.uniform(80, 200), 1)
        user_to_assistant_ratio = round(random.uniform(0.95, 1.05), 2)

        # Временные метки
        months_ago = random.randint(3, 6)
        first_message_date = datetime.now() - timedelta(days=months_ago * 30)
        last_message_date = datetime.now() - timedelta(hours=random.randint(0, 2))
        generated_at = datetime.now()

        # Формирование результата
        return DashboardStats(
            overview=OverviewStats(
                total_users=total_users,
                active_users_7d=active_users_7d,
                active_users_30d=active_users_30d,
                total_messages=total_messages,
                messages_7d=messages_7d,
                messages_30d=messages_30d,
            ),
            users=UserStats(
                premium_count=premium_count,
                premium_percentage=premium_percentage,
                regular_count=regular_count,
                by_language={
                    "ru": ru_count,
                    "en": en_count,
                    "uk": uk_count,
                    "other": other_count,
                },
            ),
            messages=MessageStats(
                avg_length=avg_length,
                first_message_date=first_message_date,
                last_message_date=last_message_date,
                user_to_assistant_ratio=user_to_assistant_ratio,
            ),
            metadata=MetadataStats(
                generated_at=generated_at,
                is_mock=True,
            ),
        )

