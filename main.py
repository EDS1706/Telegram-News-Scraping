import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# רשימת אתרי החדשות למעקב
NEWS_SITES = [
    {"name": "Ynet", "url": "https://www.ynet.co.il/home/0,7340,L-8,00.html", "selector": "a.slotTitle"},
    {"name": "TheMarker", "url": "https://www.themarker.com/", "selector": "h3 a"},
    {"name": "Calcalist", "url": "https://www.calcalist.co.il/home/0,7340,L-8,00.html", "selector": ".teaser a"},
    {"name": "Maariv", "url": "https://www.maariv.co.il/", "selector": ".news_article a"},
    {"name": "Mako", "url": "https://www.mako.co.il/", "selector": "h2 a"}
]

# מילות מפתח לחיפוש
KEYWORDS = ["McDonalds", "מק'דונלדס", "מקדונלדס", "אלעל", "EL-AL", "אל-על"]

def get_news():
    news_dict = {}

    for site in NEWS_SITES:
        try:
            response = requests.get(site["url"], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            articles = soup.select(site["selector"])
            
            for article in articles:
                title = article.get_text(strip=True)
                url_article = article["href"]

                # וידוא שהכתובת מלאה
                if not url_article.startswith("http"):
                    url_article = site["url"] + url_article

                article_id = url_article.split("/")[-1]
                article_date_timestamp = time.time()

                news_dict[article_id] = {
                    "article_date_timestamp": article_date_timestamp,
                    "title_article": title,
                    "url_article": url_article,
                }

        except Exception as e:
            print(f"שגיאה בהבאת נתונים מאתר {site['name']}: {e}")

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

def check_update():
    try:
        with open("news_dict.json", "r", encoding="utf-8") as file:
            news_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        news_dict = {}

    fresh_news = {}

    for site in NEWS_SITES:
        try:
            response = requests.get(site["url"], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            articles = soup.select(site["selector"])
            
            for article in articles:
                title = article.get_text(strip=True)
                url_article = article["href"]

                # וידוא שהכתובת מלאה
                if not url_article.startswith("http"):
                    url_article = site["url"] + url_article

                article_id = url_article.split("/")[-1]

                # חיפוש לפי מילות מפתח
                if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                    if article_id not in news_dict:
                        article_date_timestamp = time.time()
                        
                        news_dict[article_id] = {
                            "article_date_timestamp": article_date_timestamp,
                            "title_article": title,
                            "url_article": url_article,
                        }

                        fresh_news[article_id] = {
                            "article_date_timestamp": article_date_timestamp,
                            "title_article": title,
                            "url_article": url_article,
                        }

        except Exception as e:
            print(f"שגיאה בהבאת נתונים מאתר {site['name']}: {e}")

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news

def main():
    get_news()

if __name__ == "__main__":
    main()
