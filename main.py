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
    
@dp.message(lambda msg: msg.voice is not None)
async def handle_voice(message: types.Message):
    file_info = await bot.get_file(message.voice.file_id)
    file_path = file_info.file_path
    file_name = f"voice_{message.from_user.id}.ogg"

    await bot.download_file(file_path, file_name)
    await message.answer("⏳ Распознаю голос...")

    text = await voice_to_text(file_name)
    await message.answer(f"🗣 Распознанный текст:\n\n{text}")

    summary = await summarize_text(text)
    await message.answer(f"🧠 Краткая выжимка:\n\n{summary}")

    os.remove(file_name)
    if os.path.exists(file_name.replace(".ogg", ".wav")):
        os.remove(file_name.replace(".ogg", ".wav"))