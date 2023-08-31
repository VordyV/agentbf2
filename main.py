import asyncio
import logging
import sys
from os import getenv
import base64
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import html
import yaml
import client

with open('config.yaml') as f:
    CONFIG = yaml.safe_load(f)

TOKEN = CONFIG['token']

dp = Dispatcher()

USERS = {}

async def __check_permission(user_id, name, server_name):
    level_user = CONFIG['users'].get(user_id, 0)
    level_command = CONFIG['commands'].get(name, 0)
    servers_user = []

    if server_name not in CONFIG['servers']: return False

    if level_user != 0:
        servers_user = level_user['servers']
        level_user = level_user['level']

    if server_name not in servers_user: return False

    if level_user >= level_command: return True
    return False

async def __get_server(server_name):
    server = CONFIG['servers'].get(server_name, None)
    if server is None: return None

    return base64.b64decode(server.encode("utf-8")).decode("utf-8").split(":")

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    print()
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message(Command("info"))
async def command_info(message: Message):
    if not await __check_permission(message.from_user.id, "info", "local"):
        await message.answer("I'm sorry, but you don't have the right to this command.")
        return

    await message.answer("Hello!")

@dp.message(Command("rcon"))
async def command_rcon(message: Message):
    args = message.text.split()
    args.pop(0)
    if len(args) < 2:
        await message.answer("You didn't enter all the arguments: /rcon server_name rcon_command")
        return

    if not await __check_permission(message.from_user.id, "info", "local"):
        await message.answer("I'm sorry, but you don't have the right to this command.")
        return

    try:
        server = await __get_server(args[0])
    except Exception as e:
        print(e)
        await message.answer("Server data is corrupted.")
        return

    cmd = " ".join(args[1:])
    result = await client.tcp_client(server[0], int(server[1]), server[2], cmd)
    await message.answer(html.quote(result[cmd]))

@dp.message(Command("si"))
async def command_server_info(message: Message):

    args = message.text.split()
    args.pop(0)
    if len(args) < 1:
        await message.answer("You didn't enter all the arguments: /si server_name")
        return

    if not await __check_permission(message.from_user.id, "info", "local"):
        await message.answer("I'm sorry, but you don't have the right to this command.")
        return

    try:
        server = await __get_server(args[0])
    except Exception as e:
        print(e)
        await message.answer("Server data is corrupted.")
        return

    try:
        result = await client.tcp_client(server[0], int(server[1]), server[2], "bf2cc si")
    except Exception as e:
        await message.answer(str(e))
        return

    data = result["bf2cc si"]

    if "\t" not in data:
        await message.answer("The bf2cc module does not work.")
        return

    data = data.split("\t")

    __status_names = {
        1: 'Playing',
        2: 'EndGame',
        3: 'PreGame',
        4: 'Paused',
        5: 'RestartServer',
        6: 'NotConnected'
    }

    __status_em = {
        1: '🟩',
        2: '🟥',
        3: '🟧',
        4: '🟦',
        5: '🟪',
        6: '🟨'
    }

    text = "Server Information:\n\n<b>Name:</b> %s <b>Status:</b> %s %s\n<b>Online:</b> %s/%s\n<b>Map:</b> %s\n<b>Next map:</b> %s" % (
        data[7],
        __status_names[int(data[1])],
        __status_em[int(data[1])],
        data[3],
        data[2],
        data[5],
        data[6],
        )

    await message.answer(text)

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
