import typing

from getHeaders import getHeader
from requests import request, get
from typing import Dict, Any
import json
from datetime import datetime

'''
修改一半需要修改型号和name就可以了

'''
base_url = "http://172.20.251.8:31788/api/ccf/admin/{}"

headers = getHeader()

nodCode = {
    "日照": "NOD0047"
}


def baseRequest(headers: Dict[str, str], url: str, payload: Dict[str, str]) -> Any:
    response = request("POST", url, headers=headers, data=json.dumps(payload))
    if response is None:
        return None
    return response.json()


def adddevinfo(area: str, devname: str, mgmtip: str, devtype: str, devset: str, vendor: str,
               devmodel: str) -> typing.Any:
    url = base_url.format("adddevinfo")
    payload = {
        "nodeid": nodCode[area],  # 地区编码
        "devname": devname,
        "mgmtip": mgmtip,
        "mamtipv6": "",
        "devtype": devtype,
        "devset": devset,
        "vendor": vendor,
        "specialty": "PON",
        "osversion": "v1",
        "devmodel": devmodel,
        "flag": "Y",
        "testflag": "Y",
        "egion": "PON",
        "createuser": "wyc",
        "opendate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fsuinfo": {
            "fsuAcl": "127.0.0.1",
            "registerStatus": "unlogin",
            "hearbeatStatus": "unknown",
            "fsuWsurl": f"http://{mgmtip}:undefined/services/SUService?wsdl"
        }
    }

    response = baseRequest(headers=headers, url=url, payload=payload)
    code = response.get('code')
    if code == "0000":
        return "添加成功"
    return "添加失败"


# 获取设备信息
def queryalldevset(devtype: str, vendor: str) -> typing.Any:
    url = base_url.format("queryalldevset")
    params = {
        "specialty": "PON",
        "devtype": devtype,
        "vendor": vendor
    }
    respone = request("GET", url=url, params=params, headers=headers)
    return respone.json()


# 获取设备信息
def queryalldevmodel(vendor: str) -> typing.Any:
    url = base_url.format("queryalldevmodel")
    params = {
        "vendor": vendor
    }
    respone = request("GET", url=url, params=params, headers=headers)
    return respone.json()


# 获取模板信息
def queryprotocoltemplate(area: str) -> typing.Any:
    url = base_url.format("queryprotocoltemplate")
    payload = {
        "param": {
            "protocolPlateName": area,
            "protocolType": "",
            "useType": "",
            "specialty": "PON"
        },
        "page": {"pageNum": 1, "pageSize": 10}
    }

    response = baseRequest(headers=headers, url=url, payload=payload)
    code = response.get('code')
    if code == "0000":
        return response.json()
    return "获取失败"



if __name__ == '__main__':
    pass
