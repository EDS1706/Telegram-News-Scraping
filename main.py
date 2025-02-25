import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# רשימת אתרי החדשות לבדיקה
NEWS_SITES = [
    "https://www.ynet.co.il/home/0,7340,L-8,00.html",
    "https://www.themarker.com/",
    "https://www.calcalist.co.il/home/0,7340,L-8,00.html",
    "https://www.mako.co.il/",
    "https://www.maariv.co.il/",
]

# מילות המפתח למעקב
KEYWORDS = ["McDonalds", "מק'דונלדס", "מקדונלדס", "אלעל", "EL-AL", "אל-על"]

def get_news():
    news_dict = {}
    
    for site in NEWS_SITES:
        req = requests.get(site)
        soup = BeautifulSoup(req.text, "lxml")

        # חיפוש כותרות לפי תגי HTML נפוצים באתרי חדשות
        articles = soup.find_all("h2")

        for article in articles:
            title_article = article.text.strip()
            url_article = article.find("a")
            if url_article:
                url_article = url_article.get("href")

                if any(keyword in title_article for keyword in KEYWORDS):
                    article_id = url_article.split("/")[-1]
                    article_date_timestamp = time.time()

                    news_dict[article_id] = {
                        "article_date_timestamp": article_date_timestamp,
                        "title_article": title_article,
                        "url_article": url_article,
                    }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

def check_update():
    try:
        with open("news_dict.json") as file:
            news_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        news_dict = {}

    fresh_news = {}
    
    for site in NEWS_SITES:
        req = requests.get(site)
        soup = BeautifulSoup(req.text, "lxml")

        articles = soup.find_all("h2")

        for article in articles:
            title_article = article.text.strip()
            url_article = article.find("a")
            if url_article:
                url_article = url_article.get("href")

                if any(keyword in title_article for keyword in KEYWORDS):
                    article_id = url_article.split("/")[-1]

                    if article_id not in news_dict:
                        article_date_timestamp = time.time()
                        
                        news_dict[article_id] = {
                            "article_date_timestamp": article_date_timestamp,
                            "title_article": title_article,
                            "url_article": url_article,
                        }

                        fresh_news[article_id] = {
                            "article_date_timestamp": article_date_timestamp,
                            "title_article": title_article,
                            "url_article": url_article,
                        }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news

def main():
    get_news()

if __name__ == "__main__":
    main()
