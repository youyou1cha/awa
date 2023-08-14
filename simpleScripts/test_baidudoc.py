# encoding:utf-8

import requests
import base64

import requests
import json


def get_accessapi():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ghGsMugEk2rjrHbLf59O2Wv5&client_secret=pshhgBegEWwVThIPzPg5FF97XZYbWeBf"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    access_token = response.json().get("access_token")

    print(response.json())
    print(access_token)
    return access_token


def image_ocr(access_token):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
    # 二进制方式打开图片文件
    f = open('getCaptcha.svg', 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = access_token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())


if __name__ == '__main__':
    acc = get_accessapi()
    image_ocr(acc)
