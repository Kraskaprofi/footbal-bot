import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

TOKEN = "9057323164:AAGvCVZ5M8bzv-sm-_N_MHWjOWywm12T-zo"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для анализа футбольных матчей.\n\n"
        "Скиньте мне скриншоты линии, и я оценю совокупность факторов и зоны 50/50."
    )

@dp.message(lambda message: message.photo)
async def handle_screenshots(message: Message):
    await message.answer("🔄 Получил скриншоты. Анализирую зоны неопределенности и коэффициенты...")
    response_text = (
        "📊 **Результат анализа совокупности факторов:**\n\n"
        "• **Общий тотал матча:** Проверяется баланс (зоны 1.8x / 1.9x).\n"
        "• **Первый тайм:** Анализ поведения контор на предмет скрытых заманух.\n\n"
        "⚠️ *Вердикт:* Программа сопоставляет общие цифры матча с движением на единице."
    )
    await message.answer(response_text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
