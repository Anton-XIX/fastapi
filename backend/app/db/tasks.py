import logging
import os

from databases import Database
from fastapi import FastAPI

from app.core.config import DATABASE_URL

logger = logging.getLogger(__name__)


async def connect_to_db() -> None:
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else DATABASE_URL
    database = Database(DB_URL, min_size=2, max_size=10)
    try:
        await database.connect()
        logger.info("--- DB Connected ---")
        await database.disconnect()
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.error(e)
