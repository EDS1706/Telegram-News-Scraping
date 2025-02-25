import requests
from bs4 import BeautifulSoup
import datetime
import time
import json
import os

# רשימת אתרי החדשות לבדיקה
NEWS_SITES = {
    "https://www.ynet.co.il": "/home/0,7340,L-8,00.html",
    "https://www.themarker.com": "/",
    "https://www.calcalist.co.il": "/home/0,7340,L-8,00.html",
    "https://www.mako.co.il": "/",
    "https://www.maariv.co.il": "/",
}

# מילות המפתח למעקב
KEYWORDS = ["McDonalds", "מק'דונלדס", "מקדונלדס", "אלעל", "EL-AL", "אל-על", "ישראל", "ביידן"]

# יצירת קובץ JSON אם לא קיים
if not os.path.exists("news_dict.json"):
    with open("news_dict.json", "w") as file:
        json.dump({}, file)

def get_news():
    try:
        with open("news_dict.json") as file:
            news_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        news_dict = {}

    fresh_news = {}

    for base_url, path in NEWS_SITES.items():
        url = base_url + path
        try:
            req = requests.get(url, timeout=10)
            req.raise_for_status()
            soup = BeautifulSoup(req.text, "lxml")

            articles = soup.find_all("h2")

            for article in articles:
                title_article = article.text.strip()
                url_article = article.find("a")
                if url_article:
                    url_article = url_article.get("href")

                    # השלמת קישור אם הוא יחסי
                    if url_article.startswith("/"):
                        url_article = base_url + url_article

                    if any(keyword in title_article for keyword in KEYWORDS):
                        article_id = url_article.split("/")[-1]
                        article_date_timestamp = time.time()

                        if article_id not in news_dict:
                            news_dict[article_id] = {
                                "article_date_timestamp": article_date_timestamp,
                                "title_article": title_article,
                                "url_article": url_article,
                            }

                            fresh_news[article_id] = news_dict[article_id]

        except requests.RequestException as e:
            print(f"שגיאה בעת שליפת נתונים מ-{base_url}: {e}")

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news

def check_update():
    fresh_news = get_news()
    if fresh_news:
        return fresh_news
    return None

