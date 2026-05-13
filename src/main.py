import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter

from config.config import BOT_TOKEN, RECONNECTION_DELAY
from bot.handlers.commands import router as commands_router
from bot.handlers.callbacks import router as callbacks_router
from bot.handlers.processes import router as processes_router

from bot.handlers.message import router as message_router

from db.middleware import DBSessionMiddleware
from bot.middleware.sequential_processing import UserSequentialProcessingMiddleware
from bot.middleware.is_active_middleware import IsActiveMiddleware
from bot.middleware.ensure_user_middleware import EnsureUserMiddleware

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    # ROUTERS
    dp.include_router(commands_router)
    dp.include_router(callbacks_router)
    dp.include_router(message_router)
    dp.include_router(processes_router)
    
    # MIDDLEWARES
    dp.update.middleware(DBSessionMiddleware())
    dp.update.middleware(EnsureUserMiddleware())
    dp.update.middleware(IsActiveMiddleware())
    
    dp.message.middleware(UserSequentialProcessingMiddleware())
    
    # START POLLING
    while True:
        try:
            await dp.start_polling(bot)
        except TelegramNetworkError as e:
            logging.error(f"Network error: {e}. Reconnecting in {RECONNECTION_DELAY} seconds...")
            await asyncio.sleep(RECONNECTION_DELAY)
        except TelegramRetryAfter as e:
            retry_after = e.retry_after
            logging.warning(f"Rate limited. Retry after {retry_after} seconds")
            await asyncio.sleep(retry_after)
        except Exception as e:
            logging.error(f"Unexpected error: {e}. Reconnecting in {RECONNECTION_DELAY} seconds...")
            await asyncio.sleep(RECONNECTION_DELAY)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    asyncio.run(main())