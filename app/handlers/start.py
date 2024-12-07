from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.keyboards.keyboards as kb
import app.templates.cmd_message as cmd


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> Message:
    """
    Обрабатывает команду /start.

    Отправляет пользователю стартовое сообщение с приветствием и кнопкой для начала работы.
    """
    await message.answer(cmd.start_message, reply_markup=kb.main)
