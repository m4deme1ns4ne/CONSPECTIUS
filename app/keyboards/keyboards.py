from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сделать конспект')]
    ],
    resize_keyboard=True
)

confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Текст скинут", callback_data="confirmation")]
])

report_an_error = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Сообщить об ошибке", url="https://t.me/+kHxUGI-eVmhlOTY6")]
    ]
)
