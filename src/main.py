import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import BOT_TOKEN
from bot.handlers.commands import router as commands_router
from bot.handlers.callbacks import router as callbacks_router

from bot.keyboards.menu_keyboards import router as menu_router

from db.middleware import DBSessionMiddleware

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    dp.include_router(commands_router)
    dp.include_router(callbacks_router)
    dp.include_router(menu_router)
    
    dp.update.middleware(DBSessionMiddleware())
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())