import json
import datetime
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
from config import TOKEN, user_id
from main import check_update

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# פקודת /start
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["בדוק חדשות", "חמש החדשות האחרונות"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("שלום! כאן בוט החדשות שלך 📰", reply_markup=keyboard)

# כל החדשות מה-JSON
@dp.message_handler(Text(equals="בדוק חדשות"))
async def get_news(message: types.Message):
    fresh_news = check_update()

    if not fresh_news:
        await message.answer("לא נמצאו כתבות חדשות עם מילות המפתח שסיפקת.")
        return

    news_messages = []
    for _, v in sorted(fresh_news.items(), key=lambda x: x[1]['article_date_timestamp'], reverse=True):
        news_messages.append(f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']).strftime('%Y-%m-%d %H:%M:%S'))}\n{hlink(v['title_article'], v['url_article'])}")

    for news in news_messages:
        await message.answer(news)

# חמש החדשות האחרונות
@dp.message_handler(Text(equals="חמש החדשות האחרונות"))
async def get_last_five_news(message: types.Message):
    try:
        with open("news_dict.json") as file:
            news_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        news_dict = {}

    if not news_dict:
        await message.answer("אין כתבות זמינות כרגע.")
        return

    news_messages = []
    for _, v in sorted(news_dict.items(), key=lambda x: x[1]['article_date_timestamp'], reverse=True)[-5:]:
        news_messages.append(f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']).strftime('%Y-%m-%d %H:%M:%S'))}\n{hlink(v['title_article'], v['url_article'])}")

    for news in news_messages:
        await message.answer(news)

# בדיקה רציפה של חדשות חדשות ושליחתן לטלגרם
async def every_minute_news():
    while True:
        fresh_news = check_update()
        if fresh_news:
            for _, v in sorted(fresh_news.items(), key=lambda x: x[1]['article_date_timestamp'], reverse=True):
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']).strftime('%Y-%m-%d %H:%M:%S'))}\n{hlink(v['title_article'], v['url_article'])}"
                await bot.send_message(user_id, news, disable_notification=True)
        await asyncio.sleep(60)  # בדיקה כל דקה

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(every_minute_news())
    executor.start_polling(dp)
