from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer 
import asyncio
from loguru import logger
import os
from dotenv import load_dotenv

from handlers import router
from logger import file_logger


async def main():
    load_dotenv()
    file_logger()
    session = AiohttpSession(
        api=TelegramAPIServer.from_base("http://localhost:8081", is_local=True)
                            )
    bot = Bot(token=os.getenv("BOT_TOKEN"), session=session)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Бот запущен")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("Бот выключен")
