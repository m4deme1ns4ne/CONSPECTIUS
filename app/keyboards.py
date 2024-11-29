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
