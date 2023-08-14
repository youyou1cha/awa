import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from typing import Union
import json
from kafka import KafkaConsumer, KafkaProducer
from functools import partial
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
kafka_host = '192.168.175.129'
kafka_port = '9092'


# kafka生产
def send_json(host, port, value, topic):
    producer = KafkaProducer(bootstrap_servers=f"{host}:{port}")
    producer.send(topic, value)
    producer.close()


# kafka消费
def consume_json(host, port, topic):
    # 配置KafkaConsumer需要的参数
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=f"{host}:{port}",
        group_id="1",  # 指定消费组ID，可以自定义
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # 设置序列化器，这里使用JSON格式
    )

    try:
        for message in consumer:
            yield message.value  # 返回消息内容
    except KeyboardInterrupt:
        print("Consumer interrupted.")
    finally:
        consumer.close()


def extract_href_and_title(tags):
    for tag in tags:
        a_tag = tag.find('a')
        href = a_tag.get('href')
        title = a_tag.get('title')
        yield href, title


# 发送数据
def send_to_cwlConic(href, title):
    d = dict()
    d['href'] = href
    d['title'] = title
    json_d = json.dumps(d).encode('utf-8')
    sendKafka(value=json_d)


def extract_page(baseurl: str, totleNum: int):
    for num in range(2, totleNum + 1):
        yield num, baseurl.format(num)


# 返回html
def res_html_doc_byseimun(url: str) -> Union[None, str]:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    drive = webdriver.Chrome(options=chrome_options)
    drive.get(url)
    html = drive.execute_script("return document.documentElement.outerHTML")
    if html:
        return html
    else:
        return None
def res_html_doc_request(url):



sendKafka = partial(send_json, host=kafka_host, port=kafka_port)

consumeKafka = partial(consume_json, host=kafka_host, port=kafka_port)
