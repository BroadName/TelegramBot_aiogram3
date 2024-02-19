import asyncio
import logging
import configparser

from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from config_reader import config
from middlewaries.dbmiddleware import DbSession
import asyncpg
from handlers.questions import cmd_start, check_add, add_new_word, delete_word, check_to_del, lets_start, \
    try_translate, last_word
from statesform import StepsForm

db_config = configparser.ConfigParser()
db_config.read('db_config.ini')

user = db_config['params']['user']
password = db_config['params']['password']
host = db_config['params']['host']
port = db_config['params']['port']


async def create_pool():
    return await asyncpg.create_pool(user=user,
                                             password=password,
                                             database='learn_english_db',
                                             host=host,
                                             port=port,
                                             command_timeout=60)


async def main():

    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

    pool_connect = await create_pool()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.register(cmd_start, Command(commands=['start', 'run']))
    dp.message.register(check_add, F.text.lower().in_(['добавить новое слово', 'add a new word', 'add new word']))
    dp.message.register(add_new_word, StepsForm.GET_WORD)
    dp.message.register(lets_start, F.text.lower().in_(["let's start!", 'дальше', 'следующее слово', 'следующее']))
    dp.message.register(check_to_del, F.text.lower().in_(['удалить слово', 'delete word']))
    dp.message.register(delete_word, StepsForm.GET_WORD_DEL)
    dp.message.register(try_translate, StepsForm.GET_TRANSLATE)
    dp.message.register(last_word, F.text.lower().in_(['закончить', 'exit', 'выход', 'хватит']))

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
