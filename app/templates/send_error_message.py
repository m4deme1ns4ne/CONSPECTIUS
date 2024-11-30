from loguru import logger

from aiogram import Bot
from aiogram.types import Message
import app.keyboards.keyboards as kb
import app.templates.error_cmd_message as cmd


async def send_error_message(bot: Bot, msg_edit: Message) -> None:
    """Универсальная функция отправки сообщения об ошибке."""
    await bot.edit_message_text(
        chat_id=msg_edit.chat.id,
        message_id=msg_edit.message_id,
        text=cmd.error_message,
        reply_markup=kb.report_an_error,
    )
