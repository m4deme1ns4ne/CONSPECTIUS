from aiogram import Bot
from aiogram.types import Message

from .cmd_message import audio_message_accepted


async def edit_message_stage(
    bot: Bot, msg_edit: Message, text: str = None, stage: str = None
) -> None:
    """
    Обновляет сообщение с текущим статусом конспекта.

    Эта функция позволяет обновить существующее сообщение, чтобы отразить текущий
    статус документа или задачи. Сообщение может либо отображать пользовательский текст,
    либо включать предопределённое сообщение о принятии вместе с указанной стадией.

    Args:
        bot (Bot): Экземпляр Telegram-бота, используемого для отправки сообщений.
        msg_edit (Message): Оригинальный объект сообщения, который нужно изменить.
        text (str, optional): Пользовательский текст для замены содержимого оригинального сообщения. По умолчанию None.
        stage (str, optional): Информация о стадии для добавления к предопределённому сообщению о принятии. По умолчанию None.
    """
    # Убедитесь, что указано либо 'text', либо 'stage'; в противном случае возникнет исключение.
    if stage:
        message_text = (
            f"{audio_message_accepted}\nВаш конспект в статусе: {stage}"
        )
    else:
        message_text = text or "Статус не указан."

    await bot.edit_message_text(
        chat_id=msg_edit.chat.id,
        message_id=msg_edit.message_id,
        text=message_text,
    )
