import requests
from bs4 import BeautifulSoup
import datetime
import time
import json
import os
import re

# רשימת אתרי החדשות לבדיקה עם תבניות חיפוש ספציפיות
NEWS_SITES = {
    "https://www.ynet.co.il": {
        "path": "/home/0,7340,L-8,00.html",
        "article_selector": "div.slotTitle, article h2, div.title",
        "link_selector": "a"
    },
    "https://www.themarker.com": {
        "path": "/",
        "article_selector": "h2.teaser-title, article h2, div.element-image",
        "link_selector": "a"
    },
    "https://www.calcalist.co.il": {
        "path": "/home/0,7340,L-8,00.html",
        "article_selector": "h2, article h3, div.ArticleTitle",
        "link_selector": "a"
    },
    "https://www.mako.co.il": {
        "path": "/",
        "article_selector": "h2, article h3, div.title",
        "link_selector": "a"
    },
    "https://www.maariv.co.il": {
        "path": "/",
        "article_selector": "h2, article h3, div.teaser-title",
        "link_selector": "a"
    },
}

# מילות המפתח למעקב - מנרמל את הניסוח להטיות שונות
KEYWORDS = ["McDonalds", "מק'דונלדס", "מקדונלד", "אלעל", "EL-AL", "אל על", "אל-על", "ישראל", "ביידן"]

# יצירת קובץ JSON אם לא קיים
if not os.path.exists("news_dict.json"):
    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump({}, file)

def get_news():
    try:
        with open("news_dict.json", encoding="utf-8") as file:
            news_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        news_dict = {}
    
    fresh_news = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for base_url, site_config in NEWS_SITES.items():
        url = base_url + site_config["path"]
        print(f"בודק {url}...")
        
        try:
            req = requests.get(url, headers=headers, timeout=15)
            req.raise_for_status()
            
            soup = BeautifulSoup(req.text, "lxml")
            articles = soup.select(site_config["article_selector"])
            
            print(f"מצאתי {len(articles)} אלמנטים פוטנציאליים באתר {base_url}")
            
            for article in articles:
                # חיפוש כותרת
                title_article = article.text.strip()
                
                # דילוג על טקסטים קצרים מדי
                if len(title_article) < 5:
                    continue
                
                # חיפוש קישור בתוך האלמנט
                link_element = article.select_one(site_config["link_selector"])
                
                if link_element and link_element.has_attr("href"):
                    url_article = link_element["href"]
                    
                    # השלמת קישור אם הוא יחסי
                    if url_article.startswith("/"):
                        url_article = base_url + url_article
                    elif not (url_article.startswith("http://") or url_article.startswith("https://")):
                        url_article = base_url + "/" + url_article
                    
                    # בדיקה אם כותרת הכתבה מכילה מילת מפתח
                    title_lower = title_article.lower()
                    if any(keyword.lower() in title_lower for keyword in KEYWORDS):
                        print(f"מצאתי כתבה רלוונטית: {title_article}")
                        
                        # יצירת מזהה ייחודי
                        article_id = f"{base_url}_{url_article.split('/')[-1]}"
                        article_date_timestamp = time.time()
                        
                        if article_id not in news_dict:
                            news_dict[article_id] = {
                                "article_date_timestamp": article_date_timestamp,
                                "title_article": title_article,
                                "url_article": url_article,
                                "source": base_url
                            }
                            fresh_news[article_id] = news_dict[article_id]
        
        except requests.RequestException as e:
            print(f"שגיאה בעת שליפת נתונים מ-{base_url}: {e}")
        except Exception as e:
            print(f"שגיאה כללית בעת עיבוד {base_url}: {e}")
    
    # שמירת כל הכתבות במסד הנתונים
    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    
    return fresh_news

def check_update():
    print("בודק עדכוני חדשות...")
    fresh_news = get_news()
    if fresh_news:
        print(f"נמצאו {len(fresh_news)} כתבות חדשות")
        return fresh_news
    print("לא נמצאו כתבות חדשות")
    return None

if __name__ == "__main__":
    # ריצת בדיקה
    fresh_news = check_update()
    if fresh_news:
        for article_id, article in fresh_news.items():
            print(f"כותרת: {article['title_article']}")
            print(f"קישור: {article['url_article']}")
            print("----")

