import logging
import asyncio
import threading

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand, Message
import betterlogging as bl

from base_settings import base_settings
from handlers.admin.admin_router import admin_main_router
from serve import serve


def get_storage():
    return MemoryStorage()


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )


async def on_startup():
    logging.info("Starting bot")


async def on_shutdown(bot):
    logging.info("Shutdown bot")#dev


async def main():
    bot, dp = await create_bot()
    await asyncio.gather(start_bot(bot, dp), serve(bot))

async def create_bot():
    setup_logging()
    storage = get_storage()
    bot = Bot(token=base_settings.get_token())
    dp = Dispatcher(storage=storage)
    dp.include_routers(admin_main_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return bot, dp

async def start_bot(bot, dp):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=[BotCommand(command='start', description='Запустить бота')],
                              scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())