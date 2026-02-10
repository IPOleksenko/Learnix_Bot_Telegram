from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from db.session import get_db


class DBSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        with get_db():
            return await handler(event, data)
