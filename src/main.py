"""Точка входа приложения."""

import asyncio
import logging

from dotenv import load_dotenv

from .bot import TelegramBot
from .config import Config
from .conversation import Conversation
from .database import Database
from .handlers import MessageHandler
from .llm_client import LLMClient
from .migrations import run_migrations

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main() -> None:
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

    # Запускаем миграции базы данных
    try:
        logger.info("Running database migrations...")
        run_migrations(config.database_url)
    except Exception as e:
        logger.error(f"Failed to run migrations: {e}")
        return

    # Создаем компоненты приложения
    database = Database(config.database_url, config.database_timeout)
    conversation = Conversation(database)
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
