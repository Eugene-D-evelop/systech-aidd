"""Клиент для работы с LLM через OpenRouter API."""

import logging

from openai import APIError, AsyncOpenAI, Timeout

from src.config import Config

logger = logging.getLogger(__name__)


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
        self, messages: list[dict], system_prompt: str | None = None
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
            Exception: Другие ошибки
        """
        try:
            # Формируем полный список сообщений
            full_messages = []

            # Добавляем системный промпт, если указан
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})

            # Добавляем историю сообщений
            full_messages.extend(messages)

            logger.info(
                f"Sending request to LLM: {len(full_messages)} messages, "
                f"model: {self.config.openrouter_model}"
            )

            # Отправляем запрос к LLM
            response = await self.client.chat.completions.create(
                model=self.config.openrouter_model,
                messages=full_messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout,
            )

            # Извлекаем текст ответа
            answer = response.choices[0].message.content

            if not answer:
                logger.warning("LLM returned empty response")
                return "Извините, я не смог сгенерировать ответ. Попробуйте еще раз."

            logger.info(f"LLM response received, length: {len(answer)} chars")
            return answer

        except Timeout as e:
            logger.error(f"LLM request timeout: {e}", exc_info=True)
            return (
                f"⏱️ Превышено время ожидания ответа ({self.config.timeout}с). "
                "Попробуйте снова."
            )

        except APIError as e:
            logger.error(f"LLM API error: {e}", exc_info=True)
            return (
                f"❌ Ошибка API: {str(e)}\n"
                "Пожалуйста, попробуйте позже или проверьте конфигурацию."
            )

        except Exception as e:
            logger.error(f"Unexpected error in LLM request: {e}", exc_info=True)
            return (
                f"❌ Произошла непредвиденная ошибка: {str(e)}\n"
                "Пожалуйста, попробуйте позже."
            )

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

