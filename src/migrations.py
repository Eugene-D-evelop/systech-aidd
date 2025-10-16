"""Запуск миграций базы данных."""

import logging
from pathlib import Path

import psycopg

logger = logging.getLogger(__name__)


def run_migrations(database_url: str) -> None:
    """Выполнение SQL миграций.

    Args:
        database_url: URL подключения к PostgreSQL
    """
    migrations_dir = Path("migrations")

    if not migrations_dir.exists():
        logger.error(f"Migrations directory not found: {migrations_dir}")
        return

    # Получаем список файлов миграций в алфавитном порядке
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        logger.warning("No migration files found")
        return

    logger.info(f"Found {len(migration_files)} migration file(s)")

    with psycopg.connect(database_url) as conn:
        for migration_file in migration_files:
            logger.info(f"Running migration: {migration_file.name}")

            try:
                with migration_file.open("r", encoding="utf-8") as f:
                    sql = f.read()

                with conn.cursor() as cur:
                    cur.execute(sql)

                conn.commit()
                logger.info(f"Migration {migration_file.name} completed successfully")

            except Exception as e:
                logger.error(f"Migration {migration_file.name} failed: {e}")
                conn.rollback()
                raise

    logger.info("All migrations completed successfully")


if __name__ == "__main__":
    # Для запуска через python -m src.migrations
    from dotenv import load_dotenv

    from .config import Config

    load_dotenv()
    config = Config()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    run_migrations(config.database_url)


