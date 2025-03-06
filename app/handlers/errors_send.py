from aiogram import F, Router
from aiogram.types import Message

import app.keyboards.keyboards as kb
import app.templates.cmd_message as cmd


router = Router()


@router.message(F.text == "Сообщить об ошибке ❗️")
async def errors_send(message: Message) -> Message:
    await message.answer(
        cmd.error_message_send, reply_markup=kb.error_report_menu
    )
