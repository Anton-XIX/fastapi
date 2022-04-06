from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import DATABASE_URL

"""
important to cast str, otherwise it will give 'DatabaseURL' object has no attribute '_instantiate_plugins'
"""
engine = create_engine(str(DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# async def connect_to_db(app: FastAPI) -> None:
#     DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else DATABASE_URL
#     database = Database(DB_URL, min_size=2, max_size=10)  # these can be configured in config as well
#     try:
#
#         await database.connect()
#         app.state._db = database
#     except Exception as e:
#         logger.warning("--- DB CONNECTION ERROR ---")
#         logger.error(e)
#         logger.warning("--- DB CONNECTION ERROR ---")
#
#
# async def close_db_connection(app: FastAPI) -> None:
#     try:
#         await app.state._db.disconnect()
#     except Exception as e:
#         logger.warning("--- DB DISCONNECT ERROR ---")
#         logger.error(e)
#         logger.warning("--- DB DISCONNECT ERROR ---")
