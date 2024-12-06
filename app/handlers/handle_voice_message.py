from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
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
from app.core.states import MainState
from app.utils.get_length_audio import get_length_audio


router = Router()

# Конфигурационные параметры
AUDIO_UPLOAD_PATH = "/Users/aleksandrvolzanin/pet_project/site_conspectius/uploads"
DOCX_OUTPUT_PATH = "/Users/aleksandrvolzanin/pet_project/CONSPECTIUS/app/received_txt/input_file.docx"
LANGUAGES = ("en", "en_au", "en_uk", "en_us", "es", "fr", "de", "it", "pt", "nl","hi", "ja", "zh", "fi", "ko", "pl", "ru", "tr", "uk", "vi")

@router.message(F.text == "Сделать конспект 📄✨")
async def handle_summarize_request(message: Message, state: FSMContext):
    """
    Обработка запроса на создание конспекта. Отправляет инструкцию
    пользователю, как создать конспект.
    """
    # Проверка текущего состояния FSM и переход в состояние ожидания ответа (если необходимо)
    current_state = await state.get_state()
    if current_state == MainState.waiting_for_response.state:
        await message.reply("Пожалуйста, дождитесь завершения обработки предыдущего запроса.")
        return
    await state.set_state(MainState.waiting_for_response)

    if current_state == MainState.waiting_for_response.state:
        await message.reply("Пожалуйста, подождите завершение обработки предыдущего запроса. ⏳")
        return

    await message.answer(
        "1. Пришлите аудио по первой кнопке 🎧\n2. После этого нажмите на кнопку 'Аудио скинуто ✔️'",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=kb.confirmation,
    )

@router.callback_query(F.data == "select_language")
async def select_language(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_text(
        text="Выберите язык для расшифровки аудио сообщения: 🎧🌍",
        reply_markup=kb.select_language
    )

@router.callback_query(lambda callback: callback.data in LANGUAGES or callback.data == "cancel")
async def process_confirmation(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Обрабатывает запрос обратного вызова для подтверждения аудиофайла.

    Эта функция проверяет существование загруженного аудиофайла,
    транскрибирует его в текст, обрабатывает транскрипцию с помощью GPT,
    преобразует обработанный текст в файл DOCX и отправляет файл
    пользователю. 
    """ 
    # Проверка текущего состояния FSM и переход в состояние ожидания ответа (если необходимо)
    current_state = await state.get_state()
    if current_state == MainState.waiting_for_response.state:
        await callback.message.reply("Пожалуйста, дождитесь завершения обработки предыдущего запроса. 😊")
        return
    await state.set_state(MainState.waiting_for_response)

    waiting_message = await callback.message.edit_text(
        text=cmd.audio_message_accepted,
        parse_mode=ParseMode.MARKDOWN
    )

    # Проверка наличия аудиофайла
    try:
        audio_path = check_any_file_exists(AUDIO_UPLOAD_PATH)
        logger.info("Аудио найдено")
    except Exception as err:
        await state.clear()
        logger.error(f"Файл не найден: {err}")
        await send_error_message(bot, msg_edit=waiting_message,
                                 error="Файл не найден❗️")
        return

    # Распознавание аудио
    try:
        language = callback.data
        await edit_message_stage(bot, msg_edit=waiting_message, stage="Перевод аудиосообщения в текст 🎤")
        transcription = await transcribing_aai(file_path=audio_path, language=language)
        if not transcription:
            raise Exception("Транскрипция не выполнена.")
        logger.info("Аудио успешно расшифровано.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при расшифровке аудио: {err}")
        await send_error_message(bot, waiting_message,
                                 error="Произошла ошибка при расшифровке аудиофайла❗️")
        return
    
    #Определение длины аудио сообщения
    try:
        await edit_message_stage(bot, msg_edit=waiting_message, stage="Определение длины аудиосообщения 🎤")
        length_audio_files = get_length_audio(file_path=audio_path)
        logger.info("Длина аудио успешно определена.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при определении длины аудио: {err}")
        await send_error_message(bot, waiting_message,
                                 error="Произошла ошибка при определении длины аудиофайла❗️")
        return

    # Обработка расшифровки через GPT
    try:
        await edit_message_stage(bot, msg_edit=waiting_message, stage="Обработка текста нейросетью 🤖")
        ai = GPTResponse()
        conspect = await ai.processing_transcribing(transcription, length_audio=length_audio_files)
        if not conspect:
            raise Exception()
        logger.info("Конспект успешно обработан GPT.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при обработке конспекта: {err}")
        await send_error_message(bot, waiting_message,
                                 error="Произошла ошибка при обработке конспекта❗️")
        return

    # Конвертация текста в DOCX
    try:
        txt_to_docx(text=conspect)
        logger.info("Файл успешно конвертирован в .docx.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при конвертации файла: {err}")
        await send_error_message(bot, waiting_message,
                                 error="Произошла ошибка при конвертации файла в формат .docx ❗️")
        return

    # Отправка файла пользователю
    try:
        input_file = FSInputFile(DOCX_OUTPUT_PATH)
        await edit_message_stage(bot, msg_edit=waiting_message, text="Ваш конспект ☺️")
        await callback.message.answer_document(input_file)
        await state.clear()
        logger.info("Файл успешно отправлен пользователю.")
    except Exception as err:
        await state.clear()
        logger.error(f"Ошибка при отправке файла: {err}")
        await send_error_message(bot, waiting_message,
                                 error="Произошла ошибка при отправке файла вам❗️")
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
    await message.reply("Пожалуйста, нажмите на кнопку 'Сделать конспект' для создания конспекта.")
    return
