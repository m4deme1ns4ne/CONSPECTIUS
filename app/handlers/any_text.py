from aiogram import F, Router
from aiogram.types import Message


router = Router()


@router.message(F.text)
async def any_text(message: Message):
    await message.reply("Пожалуйта, выберите один из пунктов меню.")
    return
