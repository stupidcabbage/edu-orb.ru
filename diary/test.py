import asyncio

from aiogram.types import FSInputFile
from config import second_bot

photo = FSInputFile("test.png")
asyncio.run(second_bot.send_photo(1122659029, photo))
