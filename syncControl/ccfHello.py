import re
import os
from cff_d.getHeaders import get_cookies_from_chrome, getCookiesFromFile, getHeader
from cff_d.tigger import trigger
from cff_d.sync import queryresource, updatedomain


class app():
    def __init__(self):
        COOKIES_NAME = "cookies.json"
        basedir = os.path.dirname(__file__)
        cookies_path = os.path.join(basedir, COOKIES_NAME)
        get_cookies_from_chrome(cookies_path=cookies_path)
        cookies = getCookiesFromFile(cookies_path=cookies_path)
        self.headers = getHeader(cookies=cookies)
        self.filename = 'sync_file.txt'
        self.pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    def getIp(self):
        ips = []
        with open(self.filename, mode='r', encoding='utf-8') as f:
            # for line in f.readlines():
            #     match = re.search(self.pattern, line)
            #     if match:
            #         ip = match.group(0)
            #         print(ip)
            #         ips.append(ip)
            content = f.read()
            ips = re.findall(self.pattern, content)
        return set(ips)

    def extract_ips(self, text):
        ips = re.findall(r"\d+\.\d+\.\d+\.\d+", text)
        return set(ips)

    def send_to_ccf(self):
        ips = self.getIp()
        colids = []
        message = "开始处理 :"
        print(message)
        for ip in ips:
            message = "Ip地址 :   {}".format(ip)
            print(message)
            colid = queryresource(devaddress=ip, headers=self.headers)
            if colid:
                colids.append(colid)
            else:
                message = "不存在"
                print(message)
        message = "devid :   {}".format(','.join(colids))
        print(message)

        message = "开始上传 :"
        print(message)

        result = updatedomain(devids=colids, headers=self.headers)
        # result = 1

        message = "执行结果   {}".format(result)
        print(message)
        if result:
            res = trigger(headers=self.headers)
            if res:
                message = "执行成功"
                print(message)
        # message = "执行失败"
        print(message)


if __name__ == '__main__':
    app = app()
    app.send_to_ccf()
