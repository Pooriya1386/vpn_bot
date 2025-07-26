import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import register_handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

register_handlers(dp)

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())

