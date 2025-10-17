"""Pydantic модели для статистики дашборда."""

from datetime import datetime

from pydantic import BaseModel, Field


class OverviewStats(BaseModel):
    """Общая статистика использования бота."""

    total_users: int = Field(..., description="Общее количество пользователей", ge=0)
    active_users_7d: int = Field(
        ..., description="Активные пользователи за последние 7 дней", ge=0
    )
    active_users_30d: int = Field(
        ..., description="Активные пользователи за последние 30 дней", ge=0
    )
    total_messages: int = Field(..., description="Общее количество сообщений", ge=0)
    messages_7d: int = Field(..., description="Сообщения за последние 7 дней", ge=0)
    messages_30d: int = Field(..., description="Сообщения за последние 30 дней", ge=0)


class UserStats(BaseModel):
    """Статистика пользователей."""

    premium_count: int = Field(..., description="Количество Premium пользователей", ge=0)
    premium_percentage: float = Field(
        ..., description="Процент Premium пользователей", ge=0, le=100
    )
    regular_count: int = Field(..., description="Количество обычных пользователей", ge=0)
    by_language: dict[str, int] = Field(
        ..., description="Распределение пользователей по языкам"
    )


class MessageStats(BaseModel):
    """Статистика сообщений."""

    avg_length: float = Field(..., description="Средняя длина сообщения в символах", ge=0)
    first_message_date: datetime = Field(..., description="Дата первого сообщения")
    last_message_date: datetime = Field(..., description="Дата последнего сообщения")
    user_to_assistant_ratio: float = Field(
        ..., description="Соотношение сообщений пользователь/ассистент", ge=0
    )


class MetadataStats(BaseModel):
    """Метаданные о сборе статистики."""

    generated_at: datetime = Field(..., description="Время генерации статистики")
    is_mock: bool = Field(..., description="Флаг Mock данных")


class DashboardStats(BaseModel):
    """Корневая модель статистики для дашборда."""

    overview: OverviewStats = Field(..., description="Общая статистика")
    users: UserStats = Field(..., description="Статистика пользователей")
    messages: MessageStats = Field(..., description="Статистика сообщений")
    metadata: MetadataStats = Field(..., description="Метаданные")

