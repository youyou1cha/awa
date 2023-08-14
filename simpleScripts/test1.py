import requests
from bs4 import BeautifulSoup

base_url = "https://h-webtoon.com/"

res = requests.get(base_url)
soup = BeautifulSoup(res.text,'html.parser')
articles = soup.find_all('article')
d = []
for article in articles:
    tag = article.find('a')
    href = tag.get('href')
    d.append(href)

print(d)