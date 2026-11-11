import os
import asyncio
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен вашего бота
TOKEN = "9057323164:AAGvCVZ5M8bzv-sm-_N_MHWjOWywm12T-zo"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Простейший веб-сервер для удовлетворения требований Render к Web Service
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")
    def log_message(self, format, *args):
        # Отключаем лишние логи HTTP-запросов в консоли, чтобы не засорять вывод
        return

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Привет! Отправь мне скриншот матча, и я проанализирую статистику.")

@dp.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("🔍 Скриншот получен, анализирую...")

async def main():
    # Запускаем мини-веб-сервер в фоновом потоке для Render порт-биндинга
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Удаляем вебхук на случай зависших запросов и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
