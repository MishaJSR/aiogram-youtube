from aiogram import types, Router, F
from aiogram.filters import CommandStart
import validators

from base_settings import base_settings

admin_main_router = Router()
user_bot_id = base_settings.get_user_bot_id()
static_reg = "regxstate"
static_status = "progress"

@admin_main_router.message(CommandStart())
async def user_start(message: types.Message):
    await message.answer("Чтобы бот вам отправил видео с ютуб, отправьте ему ссылку")

@admin_main_router.message(F.video)
async def user_start(message: types.Message):
    print("get_video")
    try:
        if message.video:
            mes, user_id = message.caption.split(static_reg)
            await message.bot.send_video(chat_id=user_id, video=message.video.file_id)
    except:
        await message.answer(text="Ошибка, отправьте URL")

@admin_main_router.message()
async def user_start(message: types.Message):
    if message.chat.id != user_bot_id:
        if validators.url(message.text):
            await message.answer("Идёт обработка ссылки ...")
            await message.bot.send_message(chat_id=user_bot_id, text=message.text+"`"+str(message.chat.id))
        else:
            await message.answer("URL неопределён")
        print("send")

