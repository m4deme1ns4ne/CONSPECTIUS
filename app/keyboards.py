from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='Подписка')
    ]],
    input_field_placeholder="Просто загрузи аудиозапись лекции и я создам конспект..",
    resize_keyboard=True
)
