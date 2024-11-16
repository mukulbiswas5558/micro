import asyncpg
from fastapi import HTTPException
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Configure logger
logger = logging.getLogger(__name__)

async def get_db():
    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise e
