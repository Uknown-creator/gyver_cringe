import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F

from config_reader import config
# import parser

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.username}! "
        f"Это Gyver Check - бот, специально разработанный "
        f"для распознавания деталей по фото. Он может распознавать "
        f"только детали из наборов Алекса Гайвера, поскольку "
        f"был на них обучен :)\n\nЧтобы начать, просто отправьте фотографию")


@dp.message(Command("meow"))
async def cmd_meow(message: types.Message):
    await message.reply("ITшникам привет!")


@dp.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    photo_name = message.photo[-1].file_id
    await bot.download(
        message.photo[-1],
        destination=f"tmp/{photo_name}.jpg"
    )
    await message.reply(f"Ты отправил какуюто {photo_name}. Можешь поплакать об этом")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
