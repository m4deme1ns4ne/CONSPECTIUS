from aiogram import Bot
from aiogram.types import Message

from .cmd_message import audio_message_accepted


async def edit_message_stage(bot: Bot, msg_edit: Message, stage: str) -> None:
    """Универсальная функция изменения сообщения об статусе конспекта."""
    await bot.edit_message_text(
        chat_id=msg_edit.chat.id,
        message_id=msg_edit.message_id,
        text=f"""
{audio_message_accepted}
Ваш конспект готов на {stage}%
"""
    )
