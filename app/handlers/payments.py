from aiogram import F, Router
from aiogram.types import Message

import app.keyboards.keyboards as kb
import app.templates.cmd_message as cmd


router = Router()


@router.message(F.text == "Подписка 🌟")
async def payments(message: Message) -> Message:
    await message.answer(cmd.subscription, reply_markup=kb.main_menu)
