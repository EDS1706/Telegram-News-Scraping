# About
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beautifulsoup4)


Telegram bot that displays news from the site [Playground](https://www.playground.ru/misc/news)

# Installation (GNU/LINUX)

download the repository:

```bash
git clone https://github.com/ZeroNiki/Telegram-News-Scraping.git
```

Let's create a virtual environment before going to the folder:

```bash
python3 -m venv venv && source venv/bin/activate
```

install requirements:

```bash
pip install -r requirements.txt  
```

## Usage

open config.py:

```python
TOKEN = "your bot token" 

user_id = "Your user id"
```

You can get TOKEN from @botfather. And user id from @userinfobot

open main.py:

```python
def main():
    #get_news()
    print(check_update())
```
check_update() can update your news_dict.json file and add new news 

After all this. You can run bot.py and let's test. Send bot /start
