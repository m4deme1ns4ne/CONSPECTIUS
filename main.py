import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from loguru import logger
import os

from app.core.logger import file_logger
from app.handlers import (start, handle_voice_message)


@logger.catch
async def main() -> None:

    load_dotenv()
    file_logger()

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_routers(start.router,
                       handle_voice_message.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Бот запущен")
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.error("Бот выключен")
