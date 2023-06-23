import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hlink
from aiogram.dispatcher.filters import Text
from aiogram import asyncio
from config import TOKEN, user_id
from main import check_update

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)

# Начало
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние пять новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Лента новостей", reply_markup=keyboard)

# Все новости
@dp.message_handler(Text(equals="Все новости"))
async def get_news(message: types.Message):
    with open("news_dict.json") as file:
       news_dict = json.load(file)
    
    for k, v in sorted(news_dict.items()):
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'],v['url_article'])}"
        
        await message.answer(news)

# Последние пять новостей
@dp.message_handler(Text(equals="Последние пять новостей"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
       news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
       news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'],v['url_article'])}"
       await message.answer(news)

# Свежие новости
@dp.message_handler(Text(equals="Свежие новости"))
async def fresh_news(message: types.Message):
    fresh_news = check_update()
    
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'],v['url_article'])}"
            await message.answer(news)
    else:
        await message.answer("Пока что нет свежих новостей")
           
# Новости каждую минуту
async def every_menute_news():
    while True:
        fresh_news = check_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))} \n {hlink(v['title_article'],v['url_article'])}"

                # Получить свой id можно через @userinfobot !Не забудьте вписать ваш id в config.py
                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, "Нету свежих новостей")

        await asyncio.sleep(20)

            


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(every_menute_news())
    executor.start_polling(dp)