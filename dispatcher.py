import asyncio
import datetime

from logger import logger

import aiohttp

import telebot
from telebot.async_telebot import AsyncTeleBot

from config import bot_token, exchangerate_token

bot = AsyncTeleBot(bot_token)

@bot.message_handler(commands=['start'])
async def start(message: telebot.types.Message):
    text = "Приветствую! Это бот для тестового задания компании EasyBytes. Он умеет конвертировать валюты. Наберите /help для списка команд"
    await bot.send_message(message.chat.id, text)
    user = message.from_user.id
    logger.info(f"Пользователь {user} команда /start")


@bot.message_handler(commands=['help'])
async def start(message: telebot.types.Message):
    text = "Наберите /convert 100 USD to RUR."
    await bot.send_message(message.chat.id, text)
    user = message.from_user.id
    logger.info(f"Пользователь {user} команда /help")


@bot.message_handler(commands=['convert'])
async def handle_convert(message):
    user = message.from_user.id
    try:
        # Получаем валюту и сумму из сообщения пользователя
        amount = message.text.split()[1]
        from_currency = message.text.split()[2]
        to_currency = message.text.split()[4]
    except Exception as e:
        await bot.reply_to(message, f'Произошла ошибка: {str(e)}')
        logger.error(f"Пользователь {user} команда /convert")
        # Отправляем запрос к API для конвертации валют и отвечаем пользователю
    try:
        api_url = f"https://v6.exchangerate-api.com/v6/{exchangerate_token}/pair/{from_currency}/{to_currency}/{amount}/"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                e = await response.json()
        result = e["conversion_result"]
        await bot.reply_to(message, f'{amount} {from_currency} = {result} {to_currency}')
        logger.info(f"Пользователь {user} команда /convert")
    except:
        await bot.reply_to(message, f'Произошла ошибка: {str(e)}')
        logger.error(f"Пользователь {user} команда /convert")


# Обработка приветственных сообщений
@bot.message_handler(func=lambda message: message.text.lower() in ['привет', 'hello', 'здравствуйте'])
async def handle_hello(message):
# Отправка приветственного сообщения
    await bot.reply_to(message, 'Привет!')
    user = message.from_user.id
    logger.info(f"Пользователь {user} поздоровался")


# Обработка прощальных сообщений
@bot.message_handler(func=lambda message: message.text.lower() in ['пока', 'до свидания', 'goodbye'])
async def handle_goodbye(message):
    # Отправка прощального сообщения
    await bot.reply_to(message, 'Пока!')
    user = message.from_user.id
    logger.info(f"Пользователь {user} попрощался")


if __name__ == "__main__":
    print('Polling of CurrencyExchangeBot has started')
    asyncio.run(bot.polling())