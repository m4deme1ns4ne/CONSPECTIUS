from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums import ParseMode
from loguru import logger
import os

import app.keyboards.keyboards as kb
from app.templates.send_error_message import send_error_message
from app.templates.edit_message_stage import edit_message_stage
import app.templates.cmd_message as cmd
from app.core.transcribing import transcribing_aai
from app.utils.check_file_exists import check_any_file_exists
from app.utils.conversion_txt_to_docx import txt_to_docx
from app.core.handling import GPTResponse

router = Router()

# Конфигурационные параметры
AUDIO_UPLOAD_PATH = "/Users/aleksandrvolzanin/pet_project/site_conspectius/uploads"
DOCX_OUTPUT_PATH = "/Users/aleksandrvolzanin/pet_project/CONSPECTIUS/app/received_txt/input_file.docx"

@router.message(F.text == "Сделать конспект")
async def handle_summarize_request(message: Message):
    """Обрабатывает команду пользователя для создания конспекта."""
    await message.answer(
        "Скиньте конспект по [ссылке](https://89af-5-18-188-83.ngrok-free.app)",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=kb.confirmation,
    )


@router.callback_query(F.data == "confirmation")
async def process_confirmation(callback: CallbackQuery, bot: Bot):
    """Обрабатывает подтверждение и выполняет создание конспекта."""

    waiting_message = await callback.message.answer(cmd.audio_message_accepted)

    # Проверка наличия аудиофайла
    try:
        audio_path = check_any_file_exists(AUDIO_UPLOAD_PATH)
        logger.info("Аудио найдено")
    except Exception as err:
        logger.error(f"Файл не найден: {err}")
        await send_error_message(bot, msg_edit=waiting_message)
        return

    # Распознавание аудио
    try:
        await edit_message_stage(bot, msg_edit=waiting_message, stage=" Перевод аудиосообщения в текст 🎤")
        transcription = transcribing_aai(audio_path)
        logger.info("Аудио успешно расшифровано.")
    except Exception as err:
        logger.error(f"Ошибка при расшифровке аудио: {err}")
        await send_error_message(bot, waiting_message)
        return

    # Обработка расшифровки через GPT
    try:
        await edit_message_stage(bot, msg_edit=waiting_message, stage="Обработка текста нейросетью 🤖")
        ai = GPTResponse()
        conspect = await ai.processing_transcribing(transcription)
        logger.info("Конспект успешно обработан GPT.")
    except Exception as err:
        logger.error(f"Ошибка при обработке конспекта: {err}")
        await send_error_message(bot, waiting_message)
        return

    # Конвертация текста в DOCX
    try:
        txt_to_docx(text=conspect)
        logger.info("Файл успешно конвертирован в .docx.")
    except Exception as err:
        logger.error(f"Ошибка при конвертации файла: {err}")
        await send_error_message(bot, waiting_message)
        return

    # Отправка файла пользователю
    try:
        input_file = FSInputFile(DOCX_OUTPUT_PATH)
        await edit_message_stage(bot, msg_edit=waiting_message, text="Ваш конспект ☺️")
        await callback.message.answer_document(input_file)
        logger.info("Файл успешно отправлен пользователю.")
    except Exception as err:
        logger.error(f"Ошибка при отправке файла: {err}")
        await send_error_message(bot, waiting_message)
        return

    # Удаление временного файла
    try:
        os.remove(DOCX_OUTPUT_PATH)
        logger.info("Временный файл успешно удален.")
    except Exception as err:
        logger.error(f"Ошибка при удалении временного файла: {err}")
