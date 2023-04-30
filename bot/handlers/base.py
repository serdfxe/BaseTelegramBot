from aiogram import types

from aiogram.dispatcher.filters import CommandStart

from bot.misc import dp
from bot.utils.db.schemas.user import User


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    user = await User.get(User.id == message.from_user.id)
    if user:
        return await message.answer(f"Hello, {message.from_user.first_name}! You are already registered")
    
    user = await User.new(id=message.from_user.id, username=message.from_user.username)

    await message.answer(f"Hello, {message.from_user.first_name}! Now you are registered as {user.username}")
