from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router

import app.cmd_message as cmd
import app.keyboards as kb


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message) -> Message:
    await message.answer(cmd.start_message,
                         reply_markup=kb.main)