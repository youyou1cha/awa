import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import typing
# from cff_call.Decorator import check_expired
import requests
import json

url = "http://172.20.251.8:31788/views/login.html"
remote_url = "127.0.0.1:9222"
headers = {
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-locale": "zh",
    "zy_token": None,
    "x-csrf-token": None,
    "Syscode": "cc",
    "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/111.0.0.0Safari/537.36",
    # "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": None,
}


# 获取cookies
def getCookiesFromFile(cookies_path: str) -> typing.Dict:
    with open(cookies_path, "r") as f:
        cookies = json.load(f)
    return cookies


def get_handle(titlename, browser, handles):
    for handle in handles:
        browser.switch_to.window(handle)
        if titlename in browser.title:
            return handle


# 获取url的cookie然后就可以登录了
def get_cookies_from_chrome(cookies_path: str) -> typing.Dict:
    options = Options()
    options.add_experimental_option("debuggerAddress", remote_url)
    browser = webdriver.Chrome(options=options)
    handles = browser.window_handles
    # 获得页面句柄
    handle = get_handle('新一代', browser, handles)


    browser.switch_to.window(handle)
    # browser.get(url)

    # 获取当前页面的所有Cookie
    cookies = browser.get_cookies()
    # 输出Cookie
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    # return cookie_dict
    with open(cookies_path, 'w') as f:
        json.dump(cookie_dict, f)
    # return cookies_path


def str_cookies(cookies: typing.Dict) -> str:
    # cookies_str = "captcha=Os4TnnWr6z6Lz0EB7oukxw==;"
    cookies_str = ""
    for key, value in cookies.items():
        cookies_str += f"{key}={value};"
    return cookies_str[:-1]


def getHeader(cookies: typing.Dict) -> typing.Dict:
    # cookies = get_cookies_from_chrome()
    cookies_str = str_cookies(cookies)
    headers['zy_token'] = cookies['zy_token']
    headers['x-csrf-token'] = cookies['csrfToken']
    headers['Cookie'] = cookies_str

    return headers


if __name__ == '__main__':
    a = getHeader()
    print(a)
