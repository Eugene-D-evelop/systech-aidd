"""FastAPI router для веб-чата."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.chat_manager import ChatManager, ChatMode
from src.config import Config
from src.database import Database
from src.llm_client import LLMClient

logger = logging.getLogger(__name__)

# Создаем router
router = APIRouter(prefix="/api/chat", tags=["Chat"])


# Pydantic модели
class ChatMessageRequest(BaseModel):
    """Запрос на отправку сообщения в чат."""

    message: str = Field(..., description="Сообщение от пользователя", min_length=1)
    session_id: str = Field(..., description="ID сессии пользователя")
    mode: ChatMode = Field(
        default=ChatMode.NORMAL, description="Режим чата (normal/admin)"
    )


class ChatMessageResponse(BaseModel):
    """Ответ от чата."""

    response: str = Field(..., description="Ответ от AI-ассистента")
    session_id: str = Field(..., description="ID сессии")
    sql_query: str | None = Field(
        None, description="SQL запрос (только для admin режима)"
    )


class ChatHistoryMessage(BaseModel):
    """Сообщение из истории."""

    role: str = Field(..., description="Роль (user/assistant)")
    content: str = Field(..., description="Содержимое сообщения")
    sql_query: str | None = Field(None, description="SQL запрос если есть")


class ChatHistoryResponse(BaseModel):
    """История чата."""

    messages: list[ChatHistoryMessage] = Field(..., description="Список сообщений")
    session_id: str = Field(..., description="ID сессии")


# Dependency injection для ChatManager
def get_chat_manager() -> ChatManager:
    """Создание экземпляра ChatManager.

    Returns:
        ChatManager: Экземпляр менеджера чата
    """
    # Инициализируем зависимости
    config = Config()
    database = Database(config.database_url, config.database_timeout)
    llm_client = LLMClient(config)

    return ChatManager(database, llm_client)


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    chat_manager: Annotated[ChatManager, Depends(get_chat_manager)],
) -> ChatMessageResponse:
    """Отправка сообщения в чат и получение ответа.

    Args:
        request: Запрос с сообщением
        chat_manager: Менеджер чата (dependency injection)

    Returns:
        ChatMessageResponse: Ответ от AI
    """
    try:
        logger.info(
            f"New message from session {request.session_id}, mode: {request.mode}"
        )

        response, sql_query = await chat_manager.send_message(
            session_id=request.session_id, message=request.message, mode=request.mode
        )

        return ChatMessageResponse(
            response=response, session_id=request.session_id, sql_query=sql_query
        )

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error processing message: {str(e)}"
        ) from e


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_history(
    session_id: str,
    chat_manager: Annotated[ChatManager, Depends(get_chat_manager)],
    limit: int = 50,
) -> ChatHistoryResponse:
    """Получение истории чата для сессии.

    Args:
        session_id: ID сессии
        chat_manager: Менеджер чата (dependency injection)
        limit: Лимит сообщений (default: 50)

    Returns:
        ChatHistoryResponse: История сообщений
    """
    try:
        logger.info(f"Fetching history for session {session_id}, limit: {limit}")

        # Получаем историю из БД
        history_messages = await chat_manager.get_history(session_id, limit)

        # Преобразуем в Pydantic модели
        messages = [
            ChatHistoryMessage(
                role=msg["role"], content=msg["content"], sql_query=None
            )
            for msg in history_messages
        ]

        return ChatHistoryResponse(messages=messages, session_id=session_id)

    except Exception as e:
        logger.error(f"Error fetching history: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error fetching history: {str(e)}"
        ) from e


@router.delete("/history/{session_id}")
async def clear_history(
    session_id: str,
    chat_manager: Annotated[ChatManager, Depends(get_chat_manager)],
) -> dict[str, str]:
    """Очистка истории чата для сессии.

    Args:
        session_id: ID сессии
        chat_manager: Менеджер чата (dependency injection)

    Returns:
        Статус операции
    """
    try:
        logger.info(f"Clearing history for session {session_id}")

        await chat_manager.clear_history(session_id)

        return {"status": "ok", "message": f"History cleared for session {session_id}"}

    except Exception as e:
        logger.error(f"Error clearing history: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error clearing history: {str(e)}"
        ) from e

