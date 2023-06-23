import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

def get_news():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    url = "https://www.playground.ru/misc/news"
    
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    article_cards = soup.find_all("div", class_="post-content")

    news_dict = {}
    for article in article_cards:
        title_article = article.find("div", class_="post-title").text.strip()
        url_a = article.find("div", class_="post-title").find("a")
        url_article = f"{url_a.get('href')}" 

        date_article = article.find('div', class_="post-metadata").find("time").get("datetime")
        date_iso = datetime.fromisoformat(date_article)
        date_time = datetime.strftime(date_iso, "%Y-%m-%d %H:%M:%S")
        article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

        article_id = url_article.split("/")[-1]

        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "title_article": title_article,
            "url_article": url_article,
        }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)



def check_update():
    with open("news_dict.json") as file:
       news_dict = json.load(file)       
      
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    url = "https://www.playground.ru/misc/news"
    
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    article_cards = soup.find_all("div", class_="post-content")

    fresh_news = {}
    for article in article_cards:
        url_a = article.find("div", class_="post-title").find("a")
        url_article = f"{url_a.get('href')}" 
        article_id = url_article.split("/")[-1]

        if article_id in news_dict:
            continue
        else:
            title_article = article.find("div", class_="post-title").text.strip()

            date_article = article.find('div', class_="post-metadata").find("time").get("datetime")
            date_iso = datetime.fromisoformat(date_article)
            date_time = datetime.strftime(date_iso, "%Y-%m-%d %H:%M:%S")
            article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())
            
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
    #print(check_update())
    
if __name__ == "__main__":
    main()

        
