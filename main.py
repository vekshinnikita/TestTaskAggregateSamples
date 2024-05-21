

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN_TELEGRAM_BOT')

if(token is None):
    raise Exception('There is no telegram bot token')

bot = Bot(token=token)
dp = Dispatcher()

async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')