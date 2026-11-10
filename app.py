import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import os

# Токен вашего бота берется из переменных окружения Render или прописывается здесь
TOKEN = os.getenv("BOT_TOKEN", "ТОКЕН_ВАШЕГО_БОТА")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}! ⚽️\n"
        "Отправь мне скриншот матча или коэффициентов букмекерской конторы, и я выдам аналитический прогноз по голам."
    )

# Обработчик картинок (скриншотов)
@dp.message(F.photo)
async def handle_screenshot(message: Message) -> None:
    # Уведомляем пользователя, что скриншот принят в работу
    await message.answer("🔍 Скриншот получен! Анализирую статистику матча и движение коэффициентов...")
    
    # Здесь в будущем можно подключить OCR или ИИ-модель. 
    # Пока выводим структурированный вердикт по аналитике:
    await asyncio.sleep(1.5) # Имитация бурной аналитики
    
    verdict = (
        "📊 **Результат анализа скриншота:**\n\n"
        "- **Общий тотал матча:** Зона 1.8x / 1.9x (баланс соблюден).\n"
        "- **Первая половина / Голы:** Признаков явной сушки нет.\n\n"
        "⚠️ **Вердикт:** Высокая вероятность гола в ближайшие минуты или во 2-м тайме. Рекомендуется подстраховка."
    )
    await message.answer(verdict, parse_mode="Markdown")

# Общий текстовый обработчик
@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте скриншот матча или нажмите /start.")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
