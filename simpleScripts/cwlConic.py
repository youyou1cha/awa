from bs4 import BeautifulSoup
import re
import json
import pickle
import requests
import os


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        # Add more headers if needed
    }
    res = requests.get(url,headers=headers)
    if res.status_code == 200:
        return res.text
    else:
        return None


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {url} and saved as {filename}")
        return True
    else:
        print(f"Failed to download {url}")
        return False

def save_state(state):
    with open('state.pk1','wb') as f:
        pickle.dump(state,f)

def load_state():
    if os.path.exists('state.pkl'):
        with open('state.pkl','rb') as f:
            return pickle.load(f)
    return None

# 解析章节规则
def chatper_extract(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    chapters_tag = soup.select_one("#primary > div > div.g1-collection-viewport > ul")
    title_tag = soup.select_one(
        '#content > header > div.g1-row-inner > div > div.cover_wrapper > div.book_info > div.title_book > h1')
    title = title_tag.get_text()
    chapters = chapters_tag.find_all('li')
    d = dict()
    t = list()
    for chapter in (chapters):
        temp = dict()
        tag = chapter.find('a')
        temp['href'] = tag.get('href')
        temp['chapter'] = tag.get_text()
        t.append(temp)
    d['title'] = title
    d['chapters'] = t
    return d


# 解析images规则
def image_extract(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    image_one = soup.find('div', class_='g1-content-narrow g1-typography-xl entry-content')
    images = image_one.find_all('p')
    d = []
    for img in images:
        temp = dict()
        img_tag = img.find('img')
        try:
            img_url = img_tag.get('src')
            img_title = img_tag.get('title')
            temp['src'] = img_url
            temp['title'] = img_title
            d.append(temp)
        except Exception as e:
            pass
    return d


# 获取urls
def extract_page(html_doc):
    # page_content = get_data(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    articles = soup.find_all('article')
    d = []
    for article in articles:
        tag = article.find('a')
        href = tag.get('href')
        d.append(href)
    return d


# 分析
def extract_urls(url):
    # 按照流程就可以先打开这个页面，然后解析出来tile和url的json返回
    # ifFirst是不是首页，首页返回totolenum，否则不用
    print("开始 url -{}-".format(url))
    html_doc = get_data(url)
    pages = extract_page(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')
    # 翻页
    ul_tag = soup.select_one('div.pagination > ul')
    lis = ul_tag.select_one('li')
    pattern = r"共(\d+)页"
    match = re.search(pattern, lis.text)
    if match:
        total_pages = match.group(1)
    url_base = "{}page/{}"
    for num in range(2, int(total_pages) + 1):
        url1 = url_base.format(url, num)
        print(f"开始{url1}")
        html_doc = get_data(url1)
        d = extract_page(html_doc)
        pages.extend(d)

    #
    for page in pages:
        html_doc = get_data(page)
        datas = chatper_extract(html_doc)
        title = datas.get('title')

        if not os.path.exists(title):
            os.mkdir(title)
        chatpers = datas.get('chapters')
        for data in chatpers:
            chatper = data.get('chapter')
            href = data.get('href')
            path1 = os.path.join(title,chatper)
            if not os.path.exists(path1):
                os.mkdir(path1)
            html_doc = get_data(href)
            imgs = image_extract(html_doc)
            basepath = os.path.join(title,chatper)
            for img in imgs:
                title1 = img.get('title') + '.jpg'
                src = img.get('src')
                path = os.path.join(basepath,title1)
                download_image(url=src,filename=path)

if __name__ == '__main__':
    url = "https://h-webtoon.com/"

    extract_urls(url=url)
