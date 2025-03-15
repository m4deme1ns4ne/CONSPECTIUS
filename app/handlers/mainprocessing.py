import os

import httpx
from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaDocument
from loguru import logger

import app.templates.cmd_message as cmd
from app.core.handling import (ConspectConstructor, GPTClient, GPTConfig,
                               GPTResponse,)
from app.core.states import MainState
from app.core.transcribing import AssemblyAIConfig, AudioToText
from app.templates.edit_message_stage import edit_message_stage
from app.templates.send_error_message import send_error_message
from app.utils.check_file_exists import AudioManager, CheckAudioConfig
from app.utils.conversion_txt_to_docx import DocumentConfig, DocumentManager
from app.utils.get_length_audio import get_length_audio


router = Router()


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

    # Проверка текущего состояния FSM и переход в состояние ожидания ответа (если необходимо)
    current_state = await state.get_state()
    if current_state == MainState.waiting_for_response.state:
        await callback.message.reply(
            "Пожалуйста, подождите завершение обработки предыдущего запроса. ⏳"
        )
        return
    await state.set_state(MainState.waiting_for_response)

    waiting_message = await callback.message.edit_text(
        text=cmd.audio_message_accepted, parse_mode=ParseMode.MARKDOWN
    )

    telegram_id = callback.from_user.id

    # Получение языка и длины конспекта
    data_parts = callback.data.split("_")
    lenght_conspect = data_parts[0]
    language = data_parts[1]

    logger.info(f"Язык: {language}, длина конспекта: {lenght_conspect}")

    # Проверка наличия аудиофайла
    try:
        check_audio_config = CheckAudioConfig()
        audio_manager = AudioManager(config=check_audio_config)
        audio_path = audio_manager.check_audio_file(telegram_id)
        logger.debug(f"Аудио найдено: {audio_path}")
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
            stage="Обработка аудио нейросетью 🎤🤖\n\nОбычно процесс занимает от 3 до 8 минут ⏳",
        )
        # ------------------------------------------------- <- Этот кусок кода скидывает текст на транскрибаци, обычно это долго
        #                                                      поэтому, чтобы протестировать другие функции, можно просто прочитать файл,
        #                                                      чтобы не ждать долгую трансрибацию.

        #                                                      В будущем его не будет, так как будут написаны нормальные тесты(надеюсь).
        # -------------------------------------------------
        # config_transcribing = AssemblyAIConfig()
        # audio_to_text = AudioToText(config=config_transcribing)
        # transcription = await audio_to_text.transcribing(
        #     file_path=audio_path, language=language
        # )
        # if not transcription:
        #     raise Exception("Транскрипция не выполнена.")
        # -------------------------------------------------
        with open("/CONSPECTIUS/example/text.txt", "r") as file:
            transcription = file.read()
        # -------------------------------------------------
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

    # Определение длины аудио сообщения
    if lenght_conspect == "cancellength":
        try:
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
            stage="Обработка текста нейросетью ✍️🤖\n\nОбычно процесс занимает до 2-х минут. ⚡",
        )
        config_gpt = GPTConfig()
        gpt_client = GPTClient(config_gpt)
        answer_gpt = GPTResponse(gpt_client)
        conspect_constructor = ConspectConstructor(answer_gpt)
        conspect = await conspect_constructor.processing_conspect(
            text=transcription, lenght_conspect=lenght_conspect
        )
        logger.info("Конспект успешно обработан GPT.")
    except httpx.ProxyError as err:
        logger.error(f"Прокси-ошибка: {err}")
        raise Exception
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
        doc_config = DocumentConfig()
        doc_manager = DocumentManager(doc_config)
        doc_manager.txt_to_docx(conspect, telegram_id, lenght_conspect)
        doc_file_path = doc_manager.path_docx
        logger.debug("Файл успешно конвертирован в .docx.")
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
        input_file = FSInputFile(doc_file_path)
        await bot.edit_message_media(
            chat_id=waiting_message.chat.id,
            message_id=waiting_message.message_id,
            media=InputMediaDocument(
                media=input_file,
                caption="☝️🤓 Ваш конспект\n\n🤖 Нравится бот? Расскажи про него другим:\nhttps://t.me/CONSPECTIUS_bot",
            ),
        )
        await state.clear()
        logger.debug("Файл успешно отправлен пользователю.")
    except FileNotFoundError as err:
        logger.error(f"Файл не найден для переименования: {err}")
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
        os.remove(doc_file_path)
        logger.debug("Временный файл успешно удален.")
    except Exception as err:
        logger.error(f"Ошибка при удалении временного файла: {err}")
