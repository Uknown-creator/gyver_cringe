import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from keras.models import load_model
from keras_preprocessing import image
from keras_preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf
import cv2
from aiogram.filters.command import Command
from aiogram import F
import PIL
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
        f"был на них обучен :)\n\nЧтобы начать, просто отправьте фотографию.\nДля помощи используйте /help")


@dp.message(Command("meow"))
async def cmd_meow(message: types.Message):
    await message.reply("ITшникам привет!")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        f"1. Бот бесплатно может распознать до 10 фотографий деталей в неделю. "
        f"Для большего количества фотографий рекомендуем использовать нашу подписку стоимостью в 99 рублей в месяц. "
        f"Как чашка кофе. "
        f"За оформлением пишите @tr3ad0s\n\n2. Если наш бот неправильно распознает деталь на фотографии, "
        f"попробуйте сфотографировать её ближе под прямым углом. Если же распознавание все равно не происходит, "
        f"то скорее "
        f"всего, этой детали нет в нашей базе данных.\n\n3. На данный момент функция поиска деталей в проектах "
        f"дорабатывается и не работает. Ожидайте новостей.")


@dp.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    photo_name = message.photo[-1].file_id
    await bot.download(
        message.photo[-1],
        destination=f"tmp/{photo_name}.jpg"
    )
    img_path = f"tmp/{photo_name}.jpg"
    pred = predictions(img_path)
    await message.reply(f"Я думаю, что это {pred}!")


# @dp.message(Command("debug"))
# async def debug(message: types.Message, bot: Bot):
#     await message.answer()
def get_img_array(img_path, size):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=size)
    array = tf.keras.preprocessing.image.img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return array


def predictions(img_path):
    img_size = (256, 256)
    classifier = load_model('model/tmodel.h5')
    class_labels = ['прямой диод 1n4007', 'LCD дисплей 1602', 'адаптер',
                    'отсек для батарей', 'Bluetooth модуль JDY-31', 'керамический конденсатор',
                    'деталь для сервопривода', 'диск', 'герметичный датчик температуры DS18B20', 'модуль часов DS3231',
                    'электролитический конденсатор', 'потенциометр', 'беспроводной передатчик FS1000A',
                    'датчик влажности почвы', 'ультразвуковой дальномер HC-SR04',
                    'датчик температуры и влажности HTU21D',
                    'ИК-датчик', 'ИК-датчик с отслеживанием движения', 'джойстик',
                    'макетная плата', 'ножки для Arduino',
                    'светодиод', 'светодиодный матричный дисплей', 'микрофон', 'MOSFET транзистор',
                    '3-х осевой гироскоп', 'Приёмник MX RM 5V', 'Arduino Nano', 'датчик препятствий',
                    'пульт управления', 'насос', 'реле', 'резисторы', 'RFID детали',
                    'RGB диод', 'сегментальный индикатор', 'сервопривод', 'шаговый мотор', 'шина',
                    'дисплей на TM1637', 'модуль драйвера шагового мотора ULN2003', 'Wemos Mini', 'колесо',
                    'белое вращающееся колесо', 'провода',
                    'светодиодная лента WS2812B']
    try:
        preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
        img_array = preprocess_input(get_img_array(img_path, size=img_size))
        pred = np.argmax(classifier.predict(img_array), axis=1)
        predictions = class_labels[pred[0]]
        return predictions
    except Exception as e:
        return f"Проблемы с изображением\n{e}"


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
