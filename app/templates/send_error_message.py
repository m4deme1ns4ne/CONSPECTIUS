from aiogram import Bot
from aiogram.types import Message

import app.keyboards.keyboards as kb


async def send_error_message(
    bot: Bot, msg_edit: Message, error: str = None, message_to_user: str = None
) -> None:
    """Универсальная функция отправки сообщения об ошибке."""
    if error is None:
        error = "Произошла ошибка при обработке вашего аудио. ⚠️"
    if message_to_user is None:
        message_to_user = "Пожалуйста, попробуйте отправить аудио файл снова, нажав на кнопку 'Сделать конспект' или сообщите об ошибке, нажав на кнопку ниже. ⬇️"
    await bot.edit_message_text(
        chat_id=msg_edit.chat.id,
        message_id=msg_edit.message_id,
        text=f"Произошла ошибка при обработке вашего аудио. ⚠️\n\n{error}\n\n{message_to_user}",
        reply_markup=kb.report_an_error,
    )
