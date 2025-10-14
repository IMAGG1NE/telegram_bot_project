import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart


TOKEN = "7220275044:AAGksYXvHeJE7UuUTzk9FXd5Scp4iLSt0q0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}! 👋 Добро пожаловать в бота!")


async def main():
    print("Бот запущен 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
