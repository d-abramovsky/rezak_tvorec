from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import superuser
from google_drive import backup_googledrive
from database import Database
from aiogram.types import Message, FSInputFile
from aiogram.filters.command import Command
from collections import Counter

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='about',
            description='О нас'
        ),
        BotCommand(
            command='settings',
            description='Настройки'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


