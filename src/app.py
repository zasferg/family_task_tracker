
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from src.settings import TOKEN
from src.routes.tasks import  task
import asyncio
import logging
import sys

app = Dispatcher()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    app.include_router(task)
    await app.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())