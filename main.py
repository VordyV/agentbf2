import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import yaml

with open('config.yaml') as f:
    CONFIG = yaml.safe_load(f)

TOKEN = CONFIG['token']

dp = Dispatcher()

async def __check_permission(user_id, name):
    level_user = CONFIG['users'].get(user_id, 0)
    level_command = CONFIG['commands'].get(name, 0)

    if level_user >= level_command: return True
    return False

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message(Command("info"))
async def command_start_handler(message: Message):
    if not await __check_permission(message.from_user.id, "info"):
        await message.answer("I'm sorry, but you don't have the right to this command.")
        return

    await message.answer("Hello!")

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
