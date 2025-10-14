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
async def voice_to_text(voice_file_path: str) -> str:
    ogg_path = voice_file_path
    wav_path = ogg_path.replace(".ogg", ".wav")


    sound = AudioSegment.from_ogg(ogg_path)
    sound.export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь."
    except sr.RequestError:
        return "Ошибка при обращении к сервису распознавания."