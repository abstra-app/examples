"""
Create a Job to stay up-to-date on top headlines. Just paste this code.
Web scraping + delivering made easy with our scheduler.
"""

import requests
from bs4 import BeautifulSoup
import telepot


url = 'https://techcrunch.com/'
res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')
headlines = soup.find('body').find_all('h2')[:11]

news = []

for x in headlines:
    news.append(x.text.strip())

print(news)

news_string = "\n\n".join(news)

print(news_string)

token = "Your_Token"
chat_id = "Your_Chat_ID"
bot = telepot.Bot(token)


def send_message(text):
    url_req = "https://api.telegram.org/bot" + token + \
        "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())


send_message("Here are your daily Tech Crunch headlines:")
send_message(news_string)
send_message("For more, access techcrunch.com")