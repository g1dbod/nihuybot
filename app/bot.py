import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from .db import init_db, async_session, User

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            new_user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            session.add(new_user)
            await session.commit()
            await message.answer("Привет! Я сохранил тебя в базу данных. 📝")
        else:
            await message.answer("С возвращением! Ты уже в базе. 🔄")

@dp.message(F.text == "/info")
async def cmd_info(message: types.Message):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            text = (f"Твои данные в БД:\n"
                    f"ID: {user.telegram_id}\n"
                    f"Имя: {user.first_name} {user.last_name or ''}\n"
                    f"Username: @{user.username or 'не задан'}")
            await message.answer(text)
        else:
            await message.answer("Тебя нет в базе. Нажми /start")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())