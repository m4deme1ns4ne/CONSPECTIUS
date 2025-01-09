from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from app.databases.db import DatabaseConfig, DatabaseConnection, UserManagement


router = Router()


@router.message(Command("add"))
async def add_user(message: Message):
    """Добавляет подписку на месяц"""
    my_telegram_id = message.from_user.id

    if my_telegram_id != 857805093:
        return
    try:
        telegram_id = int(message.text.split()[1])
    except ValueError:
        await message.reply(
            "Неверный формат telegram_id. Используйте правильный ID."
        )
        return

    config = DatabaseConfig()
    connection = DatabaseConnection(config)
    user_manager = UserManagement(connection)

    if not await user_manager.user_exists(telegram_id):
        await user_manager.add_user(telegram_id)

    try:
        await user_manager.update_users_call_data(telegram_id, count=15)
    except Exception as err:
        logger.error(err)
    else:
        await message.reply(
            f"Добавлен пользователь с telegram_id: {telegram_id}"
        )
