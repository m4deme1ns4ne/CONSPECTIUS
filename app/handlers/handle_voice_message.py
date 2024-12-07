import os

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from loguru import logger

import app.keyboards.keyboards as kb
import app.templates.cmd_message as cmd
from app.core.handling import GPTResponse
from app.core.states import MainState
from app.core.transcribing import transcribing_aai
from app.templates.edit_message_stage import edit_message_stage
from app.templates.send_error_message import send_error_message
from app.utils.check_file_exists import check_any_file_exists
from app.utils.conversion_txt_to_docx import txt_to_docx
from app.utils.get_length_audio import get_length_audio


router = Router()

# Конфигурационные параметры
AUDIO_UPLOAD_PATH = (
    "/Users/aleksandrvolzanin/pet_project/site_conspectius/uploads"
)
DOCX_OUTPUT_PATH = "/Users/aleksandrvolzanin/pet_project/CONSPECTIUS/app/received_txt/input_file.docx"
LANGUAGES = (
    "en",
    "en_au",
    "en_uk",
    "en_us",
    "es",
    "fr",
    "de",
    "it",
    "pt",
    "nl",
    "hi",
    "ja",
    "zh",
    "fi",
    "ko",
    "pl",
    "ru",
    "tr",
    "uk",
    "vi",
)
LENGHT_CONSPECT = ("low", "medium", "high")


@router.message(F.text == "Сделать конспект 📄✨")
async def handle_summarize_request(message: Message, state: FSMContext):
    """
    Обработка запроса на создание конспекта. Отправляет инструкцию
    пользователю, как создать конспект.
    """
    # Проверка текущего состояния FSM и переход в состояние ожидания ответа (если необходимо)
    current_state = await state.get_state()
    if current_state == MainState.waiting_for_response.state:
        await message.reply(
            "Пожалуйста, дождитесь завершения обработки предыдущего запроса."
        )
        return
    await state.set_state(MainState.waiting_for_response)

    if current_state == MainState.waiting_for_response.state:
        await message.reply(
            "Пожалуйста, подождите завершение обработки предыдущего запроса. ⏳"
        )
        return

    await message.answer(
        "1. Пришлите аудио по первой кнопке 🎧\n2. После этого нажмите на кнопку 'Аудио скинуто ✔️'",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=kb.confirmation,
    )


@router.callback_query(F.data == "select_language")
async def select_language(
    callback: CallbackQuery, bot: Bot, state: FSMContext
):
    """
    Обработка callback, срабатывающего после нажатия кнопки "Аудио скинуто ✔️".
    Показывает пользователю клавиатуру для выбора языка.
    """
    try:
        await callback.message.edit_text(
            text=cmd.audio_language, reply_markup=kb.select_language
        )
    except Exception as err:
        logger.error(f"Ошибка при выборе языка: {err}")
        await state.clear()
        await send_error_message(
            bot, callback.message, error="Произошла ошибка при выборе языка❗️"
        )
        return


@router.callback_query(
    lambda callback: callback.data in LANGUAGES
    or callback.data == "cancel_language"
















)
async def select_length(
    
    
    callback: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Обработка callback, срабатывающего после нажатия кнопки "Аудио скинуто ✔️".
    Показывает пользователю клавиатуру для выбора длины конспекта.
    """
    try:

        language = callback.data
        await callback.message.edit_text(
            text=cmd.conspect_length,
            reply_markup=await kb.select_length(language),
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as err:
        logger.error(f"Ошибка при выборе длины конспекта: {err}")
        await state.clear()
        await send_error_message(
            bot, callback.message, error="Произошла ошибка при выборе языка❗️"
        )
        return


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
            transcription, lenght_conspect=lenght_conspect
        )
        if not conspect:
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


@router.message(F.text)
async def any_text(message: Message):
    await message.reply(
        "Пожалуйста, нажмите на кнопку 'Сделать конспект' для создания конспекта."
    )
    return
