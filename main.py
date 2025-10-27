import os
import asyncio
import speech_recognition as sr
from pydub import AudioSegment
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# конфигурация
BOT_TOKEN = "8144555058:AAF7IOgPsXl4Quy_5D85DLwsNqfOuwylHlM"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# голос в текст
async def voice_to_text(voice_file_path: str) -> str:
    ogg_path = voice_file_path
    wav_path = ogg_path.replace(".ogg", ".wav")

    #.ogg -> .wav
    sound = AudioSegment.from_ogg(ogg_path)
    sound.export(wav_path, format="wav")

    # Распознание речи
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

# суммаризация гс
async def summarize_text(text: str) -> str:
    try:
        LANGUAGE = "russian"
        SENTENCES_COUNT = 3

        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        summary_sentences = summarizer(parser.document, SENTENCES_COUNT)
        summary = " ".join(str(sentence) for sentence in summary_sentences)

        return summary if summary.strip() else "Текст слишком короткий для суммаризации."
    except Exception as e:
        return f"Ошибка при создании выжимки: {e}"

# команда start 
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Привет! Отправь мне голосовое сообщение — я его расшифрую и сделаю краткое резюме 🙂")


# обработка
@dp.message(lambda msg: msg.voice is not None)
async def handle_voice(message: types.Message):
    # Если длительность меньше 30 секунд — не делаем выжимку
    short_voice = message.voice.duration < 30

    file_info = await bot.get_file(message.voice.file_id)
    file_path = file_info.file_path
    file_name = f"voice_{message.from_user.id}.ogg"

    await bot.download_file(file_path, file_name)
    await message.answer("⏳ Распознаю голос...")

    text = await voice_to_text(file_name)
    await message.answer(f"🗣 Распознанный текст:\n\n{text}")

    # Делаем выжимку только если длительность >= 30 секунд
    if not short_voice:
        summary = await summarize_text(text)
        await message.answer(f"🧠 Краткая выжимка:\n\n{summary}")
    else:
        await message.answer("🎧 Сообщение короче 30 секунд — выжимку не делаю.")

    os.remove(file_name)
    wav_file = file_name.replace(".ogg", ".wav")
    if os.path.exists(wav_file):
        os.remove(wav_file)


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
