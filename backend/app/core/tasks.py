from typing import Callable

from app.db.tasks import connect_to_db


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        await connect_to_db()

    return start_app
