from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           WebAppInfo)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сделать конспект 📄✨')]
    ],
    resize_keyboard=True
)

confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ссылка для отпраки аудио", web_app=WebAppInfo(url="https://dacb-194-226-212-5.ngrok-free.app"))],
    [InlineKeyboardButton(text="Аудио скинуто ✔️", callback_data="select_language")]
])

select_language = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"), InlineKeyboardButton(text="🇦🇺 Australian English", callback_data="en_au")],
    [InlineKeyboardButton(text="☕️ British English", callback_data="en_uk"), InlineKeyboardButton(text="🇺🇸 US English", callback_data="en_us")],
    [InlineKeyboardButton(text="🇪🇸 Español", callback_data="es"), InlineKeyboardButton(text="🇫🇷 Français", callback_data="fr")],
    [InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="de"), InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="it")],
    [InlineKeyboardButton(text="🇵🇹 Português", callback_data="pt"), InlineKeyboardButton(text="🇳🇱 Nederlands", callback_data="nl")],
    [InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="hi"), InlineKeyboardButton(text="🇯🇵 日本語", callback_data="ja")],
    [InlineKeyboardButton(text="🇨🇳 中文", callback_data="zh"), InlineKeyboardButton(text="🇫🇮 Suomi", callback_data="fi")],
    [InlineKeyboardButton(text="🇰🇷 한국어", callback_data="ko"), InlineKeyboardButton(text="🇵🇱 Polski", callback_data="pl")],
    [InlineKeyboardButton(text="☕️ British English", callback_data="en_uk"), InlineKeyboardButton(text="🇹🇷 Türkçe", callback_data="tr")],
    [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="uk"), InlineKeyboardButton(text="🇻🇳 Tiếng Việt", callback_data="vi")],
    [InlineKeyboardButton(text="❌ Я не знаю", callback_data="cancel")]
])

report_an_error = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Сообщить об ошибке", url="https://t.me/+HjWqmBJSRxk2YmNi")]
    ]
)
