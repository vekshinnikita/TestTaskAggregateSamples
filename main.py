

import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router

bot = Bot(token='6561890386:AAHWRJv1g1JjPsFASbAAyewTiuTHb4u4oIk')
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