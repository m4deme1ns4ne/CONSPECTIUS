import os

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from loguru import logger

import app.templates.cmd_message as cmd
from app.core.handling import GPTResponse
from app.core.transcribing import transcribing_aai
from app.templates.edit_message_stage import edit_message_stage
from app.templates.send_error_message import send_error_message
from app.utils.check_file_exists import check_any_file_exists
from app.utils.conversion_txt_to_docx import txt_to_docx
from app.utils.get_length_audio import get_length_audio


router = Router()


# Конфигурационные параметры, нужно заменить на базу данных
AUDIO_UPLOAD_PATH = (
    "/Users/aleksandrvolzanin/pet_project/site_conspectius/uploads"
)
DOCX_OUTPUT_PATH = "/Users/aleksandrvolzanin/pet_project/CONSPECTIUS/app/received_txt/input_file.docx"


@router.callback_query(lambda callback: "_" in callback.data)
async def process_confirmation(
    callback: CallbackQuery, bot: Bot, state: FSMContext
):
    """
    Обработка callback, срабатывающего после нажатия кнопки "Длина конспекта".
    Показывает пользователю, что аудиосообщение было принято,
    инициирует процесс транскрибирования аудио, обработки текста нейросетью,
    конвертации текста в DOCX, отправки файла пользователю,
    а также логирует ошибки и отправляет сообщения об ошибках.
    """
    waiting_message = await callback.message.edit_text(
        text=cmd.audio_message_accepted, parse_mode=ParseMode.MARKDOWN
    )

    # Получение языка и длины конспекта
    data_parts = callback.data.split("_")
    lenght_conspect = data_parts[0]
    language = data_parts[1]

    logger.info(f"Язык: {language}, длина конспекта: {lenght_conspect}")

    # Проверка наличия аудиофайла
    try:
        audio_path = check_any_file_exists(AUDIO_UPLOAD_PATH)
        logger.info("Аудио найдено")
    except Exception as err:
        await state.clear()
        logger.error(f"Файл не найден: {err}")
        await send_error_message(
            bot, msg_edit=waiting_message, error="Файл не найден❗️"
        )
        return

    # Распознавание аудио
    try:
        await edit_message_stage(
            bot,
            msg_edit=waiting_message,
            stage="Перевод аудиосообщения в текст 🎤",
        )
        transcription = await transcribing_aai(
            file_path=audio_path, language=language
        )
        if not transcription:
            raise Exception("Транскрипция не выполнена.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при расшифровке аудио: {err}")
        await send_error_message(
            bot,
            waiting_message,
            error="Произошла ошибка при расшифровке аудиофайла❗️",
        )
        return

    # Если пользователь не знает желаемую длину конспекта, то происходит определение длины аудио
    # А если пользователь знает желаемую длину конспекта, то остаётся изначальная переменная lenght_conspect

    if lenght_conspect == "cancellength":
        # Определение длины аудио сообщения
        try:
            await edit_message_stage(
                bot,
                msg_edit=waiting_message,
                stage="Определение длины аудиосообщения 🎤",
            )
            lenght_conspect = get_length_audio(file_path_audio=audio_path)
            logger.info(f"Длина аудио успешно определена {lenght_conspect}")
        except Exception as err:
            await state.clear()
            logger.error(f"Ошибка при определении длины аудио: {err}")
            await send_error_message(
                bot,
                waiting_message,
                error="Произошла ошибка при определении длины аудиофайла❗️",
            )
            return

    # Обработка расшифровки через GPT
    try:
        await edit_message_stage(
            bot,
            msg_edit=waiting_message,
            stage="Обработка текста нейросетью 🤖",
        )
        ai = GPTResponse()
        conspect = await ai.processing_transcribing(
            text=transcription, lenght_conspect=lenght_conspect
        )
        if not conspect:
            logger.error("Коснпект пустой")
            raise Exception()
        logger.info("Конспект успешно обработан GPT.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при обработке конспекта: {err}")
        await send_error_message(
            bot,
            waiting_message,
            error="Произошла ошибка при обработке конспекта❗️",
        )
        return

    # Конвертация текста в DOCX
    try:
        txt_to_docx(text=conspect)
        logger.info("Файл успешно конвертирован в .docx.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при конвертации файла: {err}")
        await send_error_message(
            bot,
            waiting_message,
            error="Произошла ошибка при конвертации файла в формат .docx ❗️",
        )
        return

    # Отправка файла пользователю
    try:
        input_file = FSInputFile(DOCX_OUTPUT_PATH)
        await edit_message_stage(
            bot, msg_edit=waiting_message, text="Ваш конспект ☺️"
        )
        await callback.message.answer_document(input_file)
        await state.clear()
        logger.info("Файл успешно отправлен пользователю.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при отправке файла: {err}")
        await send_error_message(
            bot,
            waiting_message,
            error="Произошла ошибка при отправке файла вам❗️",
        )
        return

    # Удаление временного файла
    try:
        os.remove(DOCX_OUTPUT_PATH)
        os.remove(audio_path)
        logger.info("Временный файл успешно удален.")
    except Exception as err:
        logger.error(f"Ошибка при удалении временного файла: {err}")
