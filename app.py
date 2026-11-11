import os
import asyncio
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from google import genai

logging.basicConfig(level=logging.INFO)

TOKEN = "9057323164:AAGvCVZ5M8bzv-sm-_N_MHWjOWywm12T-zo"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")
    def log_message(self, format, *args):
        return

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("⚽ Привет! Отправь мне скриншот матча или букмекерской линии, и я проведу беттинг-анализ.")

@dp.message(F.photo)
async def handle_photo(message: Message):
    if not ai_client:
        await message.answer("⚠️ Ошибка: не настроен ключ GEMINI_API_KEY на сервере.")
        return

    processing_msg = await message.answer("🔍 Скриншот принят, анализирую статистику через Gemini...")
    
    try:
        # Скачиваем файл из Telegram
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        file_bytes = await bot.download_file(file.file_path)
        
        # Передаем картинку в Gemini с системным промптом
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                file_bytes.read(),
                "Ты профессиональный аналитик футбольных матчей и спортивных ставок. "
                "Проанализируй этот скриншот (статистику матча, коэффициенты или купон). "
                "Выдели ключевые показатели (удары, владение, тренды по тоталам) и дай экспертную оценку вероятности исходов."
            ]
        )
        
        await bot.edit_message_text(
            text=response.text,
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logging.error(f"AI Error: {e}")
        await bot.edit_message_text(
            text="❌ Произошла ошибка при обработке скриншота нейросетью.",
            chat_id=message.chat.id,
            message_id=processing_msg.message_id
        )

async def main():
    threading.Thread(target=run_web_server, daemon=True).start()
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Starting polling with Gemini Vision...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
