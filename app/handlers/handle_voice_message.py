from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums import ParseMode
from loguru import logger
import os

import app.keyboards as kb
import app.cmd_message as cmd
from app.transcribing import transcribing_aai
from app.etc.check_file_exists import check_any_file_exists
from app.etc.conversion_txt_to_docx import txt_to_docx
from app.handling import GPTResponse

router = Router()


@router.message(F.text == "Сделать конспект")
async def voice_message(message: Message):
    await message.answer(f"Скиньте конспект по [ссылке](https://111d-5-18-188-83.ngrok-free.app)",
                         ParseMode.MARKDOWN,
                         disable_web_page_preview=True,
                         reply_markup=kb.confirmation)


@router.callback_query(F.data == "confirmation")
async def confirmation_callback(callback: CallbackQuery, bot: Bot):
    try:
        audio = check_any_file_exists("/Users/aleksandrvolzanin/pet_project/site_conspectius/uploads")
    except Exception:
        await callback.message.answer("Файл не найден")
        return
    await callback.message.answer("""
🎧 Ваше аудиосообщение принято и обрабатывается. ⏳ Пожалуйста, подождите 5-15 минут. Спасибо за ваше терпение!
                         """)


    transcribing = transcribing_aai(audio)
    print(transcribing)
    ai = GPTResponse()
    conspect = await ai.processing_transcribing(transcribing)
    print(conspect)

    try: 
        txt_to_docx(text=conspect)
        logger.info("Файл переконвентирован из .txt в .docx")
    except Exception as err:
        await callback.message.answer(cmd.error)
        logger.error(f"Ошибка при конвертировании конспекта: {err}")

    try:
        destination_file_path = "/Users/aleksandrvolzanin/pet_project/CONSPECTIUS/app/received_txt/input_file.docx"
        # Создаем объект InputFile
        input_file = FSInputFile(destination_file_path)
        # Отправляем файл
        await callback.message.answer_document(input_file, caption="Ваш конспект: ")
        logger.info("Файл скинут")
        os.remove
    except Exception as err:
        await callback.message.answer(cmd.error)
        logger.error(f"Ошибка при пересылке файла: {err}")
