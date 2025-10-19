import logging
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.parsing_text import process_phrase
import app.templates_msg

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(app.templates_msg.starting_text)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(app.templates_msg.help_msg)

@router.message(F.text)
async def get_message(message: Message):
    try:
        result = process_phrase(message.text)
        await message.reply(f"Данные добавлены: {result}")
    except ValueError as e:
        await message.reply(f"Ошибка ввода: {str(e)}")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
        await message.reply(app.templates_msg.error_msg)