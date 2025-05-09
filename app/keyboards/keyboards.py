import os

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup, WebAppInfo,)
from dotenv import load_dotenv


load_dotenv()


URL = os.getenv("URL", "")
if not URL:
    raise ValueError(f"URL пустая: URL = {URL}")


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сделать конспект 📄✨")],
        [
            KeyboardButton(text="Поддержать проект ❤️"),
            KeyboardButton(text="Сообщить об ошибке ❗️"),
        ],
    ],
    resize_keyboard=True,
)

audio_confirmation_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Ссылка для отпраки аудио 🔗",
                web_app=WebAppInfo(url=URL),
            )
        ],
        [
            InlineKeyboardButton(
                text="Аудио скинуто ✅", callback_data="select_language"
            )
        ],
    ]
)

language_selection_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru")],
        [
            InlineKeyboardButton(
                text="🇦🇺 Australian English", callback_data="en_au"
            ),
            InlineKeyboardButton(text="🇻🇳 Tiếng Việt", callback_data="vi"),
        ],
        [
            InlineKeyboardButton(
                text="🇬🇧 British English", callback_data="en_uk"
            ),
            InlineKeyboardButton(text="🇺🇸 US English", callback_data="en_us"),
        ],
        [
            InlineKeyboardButton(text="🇪🇸 Español", callback_data="es"),
            InlineKeyboardButton(text="🇫🇷 Français", callback_data="fr"),
        ],
        [
            InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="de"),
            InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="it"),
        ],
        [
            InlineKeyboardButton(text="🇵🇹 Português", callback_data="pt"),
            InlineKeyboardButton(text="🇳🇱 Nederlands", callback_data="nl"),
        ],
        [
            InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="hi"),
            InlineKeyboardButton(text="🇯🇵 日本語", callback_data="ja"),
        ],
        [
            InlineKeyboardButton(text="🇨🇳 中文", callback_data="zh"),
            InlineKeyboardButton(text="🇫🇮 Suomi", callback_data="fi"),
        ],
        [
            InlineKeyboardButton(text="🇰🇷 한국어", callback_data="ko"),
            InlineKeyboardButton(text="🇵🇱 Polski", callback_data="pl"),
        ],
        [
            InlineKeyboardButton(text="🇹🇷 Türkçe", callback_data="tr"),
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="uk"),
        ],
        [
            InlineKeyboardButton(
                text="🤖 Определить автоматически",
                callback_data="cancel_language",
            )
        ],
    ]
)


async def select_length(language: str):
    length_selection_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Саммари",
                    callback_data=f"low_{language}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📚 Подробный конспект",
                    callback_data=f"high_{language}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🤖 Определить автоматически",
                    callback_data=f"cancellength_{language}",
                )
            ],
        ]
    )
    return length_selection_menu


error_report_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сообщить об ошибке", url="https://t.me/+HjWqmBJSRxk2YmNi"
            )
        ]
    ]
)


donate_url = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Единоразовый донат",
                url="https://pay.cloudtips.ru/p/ecc9c8ca",
            )
        ],
        [
            InlineKeyboardButton(
                text="Регулярный платеж",
                url="https://t.me/tribute/app?startapp=sq4G",
            )
        ],
    ]
)
