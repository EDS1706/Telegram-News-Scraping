import requests
from bs4 import BeautifulSoup
from datetime import datetime
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
KEYWORDS = ["McDonalds", "מק'דונלדס", "מקדונלדס", "אלעל", "EL-AL", "אל-על"]

# וידוא שקובץ ה-JSON קיים
if not os.path.exists("news_dict.json"):
    with open("news_dict.json", "w") as file:
        json.dump({}, file)

# הגדרת Headers כדי למנוע חסימות
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_news():
    """איסוף חדשות מכל האתרים ושמירתם בקובץ JSON"""
    try:
        with open("news_dict.json", "r") as file:
            news_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        news_dict = {}

    new_articles = {}

    for base_url, path in NEWS_SITES.items():
        url = base_url + path
        try:
            req = requests.get(url, headers=HEADERS)
            req.raise_for_status()
            soup = BeautifulSoup(req.text, "lxml")

            # חיפוש כותרות
            articles = soup.find_all("h2")
            for article in articles:
                title_article = article.text.strip()
                url_article = article.find("a")
                
                if url_article:
                    url_article = url_article.get("href")

                    # השלמת קישור אם הוא יחסי
                    if url_article.startswith("/"):
                        url_article = base_url + url_article

                    # בדיקה אם הכותרת כוללת מילת מפתח
                    if any(keyword in title_article for keyword in KEYWORDS):
                        article_id = url_article.split("/")[-1]
                        article_date_timestamp = time.time()

                        if article_id not in news_dict:
                            news_dict[article_id] = {
                                "article_date_timestamp": article_date_timestamp,
                                "title_article": title_article,
                                "url_article": url_article,
                            }
                            new_articles[article_id] = news_dict[article_id]
                            print(news_dict)  # הדפס את הכתבות שנמצאו


        except requests.RequestException as e:
            print(f"שגיאה בגישה לאתר {base_url}: {e}")

    # שמירה לקובץ JSON
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    print(f"נמצאו {len(new_articles)} כתבות חדשות.")
    return new_articles

def check_update():
    """בודק אם נוספו חדשות חדשות שלא היו בקובץ JSON"""
    try:
        with open("news_dict.json", "r") as file:
            news_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        news_dict = {}

    fresh_news = get_news()

    return fresh_news

def main():
    fresh_news = check_update()
    print(f"{len(fresh_news)} כתבות חדשות נשמרו.")

if __name__ == "__main__":
    main()
    print("החדשות נאספו בהצלחה!")
