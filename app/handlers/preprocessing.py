from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

import app.keyboards.keyboards as kb
import app.templates.cmd_message as cmd
from app.core.states import MainState
from app.templates.send_error_message import send_error_message


router = Router()

# Конфигурационные параметры, нужно заменить на базу данных
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
        reply_markup=kb.audio_confirmation_menu,
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
            text=cmd.audio_language, reply_markup=kb.language_selection_menu
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
async def select_length(callback: CallbackQuery, bot: Bot, state: FSMContext):
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


@router.message(F.text)
async def any_text(message: Message):
    await message.reply(
        "Пожалуйста, нажмите на кнопку 'Сделать конспект' для создания конспекта."
    )
    return
