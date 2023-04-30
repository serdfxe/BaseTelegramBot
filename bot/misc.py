from aiogram import Bot, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.message_handlers.once = True


def setup():
    from bot import filters, middlewares
    
    # filters.setup(dp)
    # middlwares.setup(dp)

    import bot.handlers

