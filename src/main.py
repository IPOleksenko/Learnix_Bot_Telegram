import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import BOT_TOKEN
from bot.handlers.commands import router as commands_router
from bot.handlers.callbacks import router as callbacks_router
from bot.handlers.processes import router as processes_router

from bot.handlers.message import router as message_router

from db.middleware import DBSessionMiddleware
from bot.middleware.sequential_processing import UserSequentialProcessingMiddleware
from bot.middleware.is_active_middleware import IsActiveMiddleware

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    dp.include_router(commands_router)
    dp.include_router(callbacks_router)
    dp.include_router(message_router)
    dp.include_router(processes_router)
    
    dp.message.middleware(UserSequentialProcessingMiddleware())
    dp.update.middleware(IsActiveMiddleware())
    dp.update.middleware(DBSessionMiddleware())
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())