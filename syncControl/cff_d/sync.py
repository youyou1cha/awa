import typing

# from getHeaders import getHeader
from requests import request
from typing import Dict, Any
import json

base_url = "http://172.20.251.8:31788/api/ccf/admin/{}"

# headers = getHeader()


def baseRequest(headers: Dict[str, str], url: str, payload: Dict[str, str]) -> Any:
    response = request("POST", url, headers=headers, data=json.dumps(payload))
    if response is None:
        return None
    return response.json()


def queryresource(devaddress:str,headers:typing.Dict) -> typing.Any:
    url = base_url.format("queryresource")
    payload = {
        "param": {
            "colCode": "",
            "colName": "",
            "protocolPlateName": "",
            "testStatus": "",
            "isvalid": "Y",
            "specialty": "PON",
            "protocolType": "snmp",
            "devtype": "",
            "devset": "",
            "nodeid": None,
            "devmodel": "",
            "mgmtip": devaddress,
            "devname": "",
            "netUserId": ""
        },
        "page": {
            "pageNum": 1,
            "pageSize": 10
        }
    }
    response = baseRequest(headers=headers, url=url, payload=payload)
    records = response.get('data').get('records')
    if records is []:
        return None
    colid = ""
    for record in records:
        a = record.get('mgmtip')
        if a == devaddress:
            colid = record.get("colid")
    return colid


def updatedomain(devids:typing.List,headers:typing.Dict) -> typing.Any:
    url = base_url.format("updatedomain")
    payload = {
        "domainCode": "PON_COL_snmp_OLT_rand",
        "domainName": "PON专业SNMP采集OLT_手工采集某设备手动sg",
        "colIdList": devids,
        "serverCodeList": [
            "unios-cc-col-pon"
        ],
        "specialty": "PON",
        "useType": "COL",
        "protocolType": "snmp",
        "devtype": "",
        "devset": "",
        "nodeid": None,
        "mode": "resource",
        "relationDevset": ""
    }

    response = baseRequest(headers=headers, url=url, payload=payload)
    code = response.get('code')
    if code == "0000":
        return True

    return False


if __name__ == '__main__':
    address = "10.63.197.139"
    address1 = "10.19.251.145"
    colid = queryresource(devaddress=address)
    colid1 = queryresource(devaddress=address1)
    print(colid)
    devids = []
    devids.append(colid)
    devids.append(colid1)
    a = updatedomain(devids=devids)
    print(a)
