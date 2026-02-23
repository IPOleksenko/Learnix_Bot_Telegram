import asyncio
from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

# Global dictionary with asyncio.Lock for each user
_user_locks = {}


def _get_user_lock(user_id: int) -> asyncio.Lock:
    """Get or create a Lock for the user"""
    if user_id not in _user_locks:
        _user_locks[user_id] = asyncio.Lock()
    return _user_locks[user_id]


class UserSequentialProcessingMiddleware(BaseMiddleware):
    """
    Middleware for sequential processing of each user's messages.
    
    Different users process commands in parallel,
    but for a single user commands are executed sequentially.
    """
    
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        lock = _get_user_lock(user_id)
        
        async with lock:
            return await handler(event, data)