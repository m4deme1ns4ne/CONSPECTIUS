import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from loguru import logger

from app.core.logger import file_logger
from app.handlers import (admin_handlers, any_text, mainprocessing, payments,
                          preprocessing, start,)


@logger.catch
async def main() -> None:

    load_dotenv()
    file_logger()

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        admin_handlers.router,
        preprocessing.router,
        mainprocessing.router,
        payments.router,
        any_text.router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Бот запущен")
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.error("Бот выключен")
