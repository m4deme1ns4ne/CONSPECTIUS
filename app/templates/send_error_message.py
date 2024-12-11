from aiogram import Bot
from aiogram.types import Message

import app.keyboards.keyboards as kb

from .cmd_message import error_message


async def send_error_message(
    bot: Bot, msg_edit: Message, error: str = None, message_to_user: str = None
) -> None:
    """Универсальная функция отправки сообщения об ошибке.

    Args:
        bot (Bot): Экземпляр Telegram-бота, используемого для отправки сообщений.
        msg_edit (Message): Оригинальный объект сообщения, который нужно изменить.
        error (str, optional): Ошибка, которую нужно показать пользователю. Если такой нету, то показывается заглушка.
        message_to_user (str, optional): Сообщение пользователю. Если его нету, то показывается заглушка.
    """
    if error is None:
        error = "Произошла ошибка при обработке вашего аудио. ⚠️"
    if message_to_user is None:
        message_to_user = error_message

    await bot.edit_message_text(
        chat_id=msg_edit.chat.id,
        message_id=msg_edit.message_id,
        text=f"Произошла ошибка при обработке вашего аудио. ⚠️\n\n{error}\n\n{message_to_user}",
        reply_markup=kb.error_report_menu,
    )
