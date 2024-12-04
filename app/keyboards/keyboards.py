from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           WebAppInfo)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сделать конспект')]
    ],
    resize_keyboard=True
)

confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ссылка для отпраки аудио", web_app=WebAppInfo(url="https://fc38-5-18-188-83.ngrok-free.app"))],
    [InlineKeyboardButton(text="Аудио скинуто ✔️", callback_data="confirmation")]
])

report_an_error = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Сообщить об ошибке", url="https://t.me/+kHxUGI-eVmhlOTY6")]
    ]
)
