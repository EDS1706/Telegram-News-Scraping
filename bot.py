import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
import asyncio
from config import TOKEN, user_id
from main import check_update

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# התחלה
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["כל החדשות", "5 חדשות אחרונות", "חדשות עדכניות"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("📢 בחר אפשרות:", reply_markup=keyboard)

# כל החדשות
@dp.message_handler(Text(equals="כל החדשות"))
async def get_news(message: types.Message):
    with open("news_dict.json") as file:
       news_dict = json.load(file)
    
    for k, v in sorted(news_dict.items()):
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'],v['url_article'])}"
        await message.answer(news)

# 5 חדשות אחרונות
@dp.message_handler(Text(equals="5 חדשות אחרונות"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
       news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
       news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'],v['url_article'])}"
       await message.answer(news)

# חדשות עדכניות
@dp.message_handler(Text(equals="חדשות עדכניות"))
async def fresh_news(message: types.Message):
    fresh_news = check_update()
    
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'],v['url_article'])}"
            await message.answer(news)
    else:
        await message.answer("🔍 אין חדשות חדשות כרגע.")

# בדיקת חדשות בכל 20 שניות
async def every_minute_news():
    while True:
        fresh_news = check_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'],v['url_article'])}"
                await bot.send_message(user_id, news, disable_notification=True)

        await asyncio.sleep(20)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(every_minute_news())
    executor.start_polling(dp)
