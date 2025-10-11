"""Клиент для работы с LLM через OpenRouter API."""

import logging
from typing import Any

from openai import APIError, APITimeoutError, AsyncOpenAI

from .config import Config

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Базовое исключение для ошибок LLM."""

    pass


class LLMClient:
    """Класс для взаимодействия с LLM через OpenRouter."""

    def __init__(self, config: Config):
        """Инициализация клиента LLM.

        Args:
            config: Конфигурация приложения
        """
        self.config = config
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=config.openrouter_api_key,
        )
        logger.info(f"LLM client initialized with model: {config.openrouter_model}")

    async def get_response(
        self, messages: list[dict[str, str]], system_prompt: str | None = None
    ) -> str:
        """Получение ответа от LLM.

        Args:
            messages: История сообщений в формате OpenAI API
            system_prompt: Системный промпт (опционально)

        Returns:
            Ответ от LLM

        Raises:
            Timeout: Если запрос превысил таймаут
            APIError: Если произошла ошибка API
            LLMError: Другие ошибки LLM (пустой ответ, неожиданные ошибки)
        """
        # Формируем полный список сообщений
        full_messages: list[dict[str, Any]] = []

        # Добавляем системный промпт, если указан
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})

        # Добавляем историю сообщений
        full_messages.extend(messages)

        logger.info(
            f"Sending request to LLM: {len(full_messages)} messages, "
            f"model: {self.config.openrouter_model}"
        )

        try:
            # Отправляем запрос к LLM
            response = await self.client.chat.completions.create(
                model=self.config.openrouter_model,
                messages=full_messages,  # type: ignore[arg-type]
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout,
            )

            # Извлекаем текст ответа
            answer = response.choices[0].message.content

            if not answer:
                logger.warning("LLM returned empty response")
                raise LLMError("Empty response from LLM")

            logger.info(f"LLM response received, length: {len(answer)} chars")
            return answer

        except (APITimeoutError, APIError):
            # Пробрасываем специфичные ошибки как есть
            raise

        except Exception as e:
            # Оборачиваем неожиданные ошибки в LLMError
            logger.error(f"Unexpected error in LLM request: {e}", exc_info=True)
            raise LLMError(f"Unexpected error: {e}") from e

    async def test_connection(self) -> bool:
        """Тестирование подключения к LLM API.

        Returns:
            True если подключение успешно, False иначе
        """
        try:
            test_messages = [{"role": "user", "content": "test"}]
            await self.get_response(test_messages, system_prompt="Reply with 'ok'")
            logger.info("LLM connection test successful")
            return True
        except Exception as e:
            logger.error(f"LLM connection test failed: {e}")
            return False
