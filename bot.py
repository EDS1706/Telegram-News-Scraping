import os
import json
import datetime
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
from main import check_update

# קבלת משתנים מהסביבה
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # ה-Token של הבוט
WEBHOOK_HOST = os.getenv("WEBHOOK_URL")  # כתובת ה-Render שלך
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 5000))

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# פקודה /start
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["בדוק חדשות", "חמש החדשות האחרונות"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("שלום! כאן בוט החדשות שלך 📰", reply_markup=keyboard)

# כל החדשות מה-JSON
@dp.message_handler(Text(equals="בדוק חדשות"))
async def get_news(message: types.Message):
    with open("news_dict.json") as file:
       news_dict = json.load(file)
    
    for k, v in sorted(news_dict.items()):
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'], v['url_article'])}"
        await message.answer(news)

# חמש החדשות האחרונות
@dp.message_handler(Text(equals="חמש החדשות האחרונות"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
       news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'], v['url_article'])}"
        await message.answer(news)

# בדיקה רציפה של חדשות חדשות ושליחתן לטלגרם
async def every_minute_news():
    while True:
        fresh_news = check_update()
        if fresh_news:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'], v['url_article'])}"
                await bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), news, disable_notification=True)
        await asyncio.sleep(60)  # בדיקה כל דקה

# פונקציות לאתחול וסגירה של Webhook
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

# הגדרת Webhook עם aiohttp
app = web.Application()
app.router.add_post(WEBHOOK_PATH, lambda request: dp.process_update(types.Update.de_json(request.text)))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(every_minute_news())

    from aiogram.utils.executor import start_webhook
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
