from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram import F, Router
import os
from datetime import datetime, timedelta

from cmd_message import start_message, subscription
import keyboards as kb
from main_processing import main_processing
from conversion_txt_to_docx import txt_to_docx
from loguru import logger
from cmd_message import error
from database import insert_payment_data
from database.check_subscription_status import check_subscription_status


router = Router()


# Обработчик команды /start
@logger.catch
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(start_message, reply_markup=kb.main)


# # Обработчик аудиосообщений
# @router.message(F.audio | F.voice)
@router.message(F.audio)
async def handle_voice_message(message: Message):
    global telegram_id
    telegram_id = message.from_user.id

    # Проверка статуса подписки
    if not check_subscription_status(telegram_id):
        await message.answer("Ваша подписка не активирована. Пожалуйста, активируйте подписку для использования этой функции.")
        return

    voice = message.audio.file_id
    
    # Получаем объект File по file_id
    try:
        file = await message.bot.get_file(voice)
        logger.info(f"Файл получен: {file.file_id}")
    except Exception as err:
        await message.answer(error)
        logger.error(f"Ошибка при скачивании файла: {err}")

    # Скачиваем файл
    file_path = file.file_path
    download_path = f"/home/alexandervolzhanin/pet-project/CONSPECTIUS/app/audio/{telegram_id}.mp3"

    await message.bot.download_file(file_path, download_path)

    await message.answer("""
🎧 Ваше аудиосообщение принято и обрабатывается. ⏳ Пожалуйста, подождите 5-15 минут. Спасибо за ваше терпение!
                         """)

    logger.info(f"Аудиосообщение сохранено")

    try:
        conspect = main_processing()
        
    except Exception as err:
        await message.answer(error)

    logger.info(f"Конспект получен")

    # Сохранение файла в .docx
    try:
        txt_to_docx(conspect)
        logger.info("Файл переконвентирован из .txt в .docx")

    except Exception as err:
        await message.answer(error)
        logger.error(f"Ошибка при конвертировании конспекта: {err}")

    try:
        # Путь к вашему файлу
        file_path = f"/home/alexandervolzhanin/pet-project/CONSPECTIUS/app/received_txt/{telegram_id}.docx"
        # Создаем объект InputFile
        input_file = FSInputFile(file_path)
        # Отправляем файл
        await message.reply_document(input_file, caption="Ваш конспект: ")

        logger.info("Файл скинут")

    except Exception as err:
        await message.answer(error)
        logger.error(f"Ошибка при пересылке файла: {err}")

    try:
        os.remove(file_path)
        logger.info(f"Файл {telegram_id} удалён")
    except Exception as err:
        logger.error(f"Ошибка при удалении аудио: {err}")


@router.message(F.text == "/pay")
async def process_payment(message: Message):
    telegram_id = message.from_user.id
    payment_date = datetime.now()
    subscription_end_date = payment_date + timedelta(days=30)

    insert_payment_data(telegram_id, payment_date, subscription_end_date, subscription_status=True)

    await message.answer("Оплата успешно проведена!")


@logger.catch
@router.message(F.text == "Подписка")
async def subscription_message(message: Message):
    await message.answer(subscription)
