from aiogram import F, Router
from aiogram.types import Message

import app.keyboards.keyboards as kb
import app.templates.cmd_message as cmd


router = Router()


@router.message(F.text == "Поддержать проект ❤️")
async def donate(message: Message) -> Message:
    await message.answer(cmd.donate, reply_markup=kb.donate_url)
