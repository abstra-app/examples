"""
Create a Job to stay up-to-date on top headlines. Just paste this code.
Web scraping + delivering made easy with our scheduler.
"""
import os
import requests
from bs4 import BeautifulSoup
import telepot
from dotenv import load_dotenv

load_dotenv()
url = "https://techcrunch.com/"
res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")
headlines = soup.find("body").find_all("h2")[:11]

news = []

for x in headlines:
    news.append(x.text.strip())


news_string = "\n\n".join(news)


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
print(TELEGRAM_BOT_TOKEN)
print(CHAT_ID)

def send_message(text):
    url_req = (
        "https://api.telegram.org/bot"
        + TELEGRAM_BOT_TOKEN
        + "/sendMessage"
        + "?chat_id="
        + "-1002106167565"
        + "&text="
        + text
    )
    print(url_req)
    results = requests.get(url_req)
    print(results.json())


send_message("Hello")
send_message(news_string)
