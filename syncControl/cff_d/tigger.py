import json
import typing

from requests import request


def trigger(headers: typing.Dict) -> typing.Any:
    url = "http://172.20.251.8:31488/unios-job-admin/jobinfo/trigger"
    url1 = "http://unios-pxm-dispatch:32013/dispatch/api/v1/schedulecc?taskid=2022110228488189952&strategyid=202109298029480960&tempaleid=PON_CFG_snmp_zhengshi&domain=PON_COL_snmp_OLT_rand&datareportid=202105101237187584&strategytype=CYCLE&supplymenttime=null&coltype=CFG&action=1&period=}"
    payload = {
        "id": 328,
        # "executorParam": urllib.parse.urlencode(url1)
        "executorParam": url1
    }
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    headers['X-Requested-With'] = "XMLHttpRequest"
    response = request("POST", url, headers=headers, data=payload)
    print(response.json())
    # {"code": 200, "msg": null, "content": null}
    if response.json().get("code") == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    a = trigger()
    print(a)
