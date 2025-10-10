"""Точка входа приложения."""

import asyncio
import logging

from dotenv import load_dotenv

from src.bot import TelegramBot
from src.config import Config
from src.conversation import Conversation
from src.handlers import MessageHandler
from src.llm_client import LLMClient

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    """Главная функция приложения."""
    # Загружаем переменные окружения из .env
    load_dotenv()

    # Загружаем конфигурацию
    try:
        config = Config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return

    # Создаем компоненты приложения
    conversation = Conversation()
    llm_client = LLMClient(config)
    bot = TelegramBot(config)
    message_handler = MessageHandler(config, llm_client, conversation)

    # Регистрируем обработчики
    bot.register_handlers(message_handler)

    # Запускаем бота
    logger.info("Starting bot polling...")
    await bot.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)

