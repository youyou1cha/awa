import typing

from getHeaders import getHeader, get_cookies_from_chrome, getCookiesFromFile
from requests import request, get
from typing import Dict, Any
import json
from datetime import datetime

'''
按照流程来说，分成OUN新装和OLT新装；
OUN - IP 地区 型号 细类 -  添加采控源
OLT 添加 - IP  地区 型号 细类  采控源 管理域
'''
base_url = "http://172.20.251.8:31788/api/ccf/admin/{}"

# coo = get_cookies_from_chrome("cookies.json")
cco = getCookiesFromFile("cookies.json")
headers = getHeader(cco)

nodCode = {
    "烟台": "NOD0042"
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


#  获取devset DEV_PON_OLT_HW_COM
def queryalldevset(devtype: str, vendor: str) -> typing.Any:
    url = base_url.format("queryalldevset")
    params = {
        "specialty": "PON",
        "devtype": devtype,
        "vendor": vendor
    }
    respone = request("GET", url=url, params=params, headers=headers)
    return respone.json()


# 获取queryalldevmodel MA5800T
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
        return response
    return "获取失败"


# 获取devid
def querydevinfoforprotocol(mgmtip: str,protocolPlateId:str) -> typing.Any:
    url = base_url.format("querydevinfoforprotocol")
    payload = {
        "param": {
            "devname": "",
            "mgmtip": mgmtip,
            "devtype": "",
            "devset": "",
            "specialty": "PON",
            "protocol_plate_id": protocolPlateId,
            "testflag": "",
            "flag": "",
            "devmodel": "",
            "vendor": "",
            "nodeid": None
        },
        "page": {"pageNum": 1, "pageSize": 10}
    }

    response = baseRequest(headers=headers, url=url, payload=payload)
    code = response.get('code')
    if code == "0000":
        return response
    return "获取失败"


# 添加采控源
def addresource(protocolPlateId: str, devid: str, colCode: str, colName: str) -> typing.Any:
    url = base_url.format("addresource")
    payload = [
        {
            "protocolPlateId": protocolPlateId,
            "specialty": "PON",
            "devid": devid,
            "colCode": colCode,
            "colName": colName,
            "testStatus": "未测试"
        }
    ]

    response = baseRequest(headers=headers, url=url, payload=payload)
    code = response.get('code')
    if code == "0000":
        return "添加成功"
    return "获取失败"


# 添加管理域


if __name__ == '__main__':
    area = "烟台"
    mgmtip = "10.19.252.24"
    devname = f"{area}{mgmtip}"
    vendor = "HW"
    devmodelPartal = "5800"
    devmodel = ""
    devtype = "DEV_PON_OLT"
    devset = ""

    # devsets = queryalldevset(devtype=devtype, vendor=vendor).get("data")
    # devmodels = queryalldevmodel(vendor=vendor).get("data")

    # for d in devsets:
    #     if devmodelPartal in d.get("devsetDesc"):
    #         devset = d.get("devset")
    # for m in devmodels:
    #     if devmodelPartal in m.get("devmodel"):
    #         devmodel = m.get("devmodel")
    #
    # result = adddevinfo(area=area, devname=devname, mgmtip=mgmtip, devtype=devtype, devset=devset, vendor=vendor,
    #                     devmodel=devmodel)
    # print(result)
    protocolPlateId = ""
    protocolPlateName = ""
    templates = queryprotocoltemplate(area=area)
    for temp in templates.get("data").get("records"):
        if "OLT" in devtype:
            print("aa")
            if "PON" in temp.get("protocolPlateName"):
                protocolPlateId = temp.get("protocolPlateId")
                protocolPlateName = temp.get("protocolPlateName")
        if "ONU" in devtype:
            if "FTTB" in temp.get("protocolPlateName"):
                protocolPlateId = temp.get("protocolPlateId")
                protocolPlateName = temp.get("protocolPlateName")

    devid = ""
    devids = querydevinfoforprotocol(mgmtip=mgmtip,protocolPlateId=protocolPlateId)
    for demp in devids.get("data").get("records"):
        if mgmtip == demp.get("mgmtip"):
            devid = demp.get("devid")
    # protocolPlateId: str, devid: str, colCode: str, colName: str
    colCode = f"{devid}_{protocolPlateId}"
    colName = f"{devname}_{protocolPlateName}"
    a = addresource(protocolPlateId=protocolPlateId,devid=devid,colCode=colCode,colName=colName)
    print(a)