import json
import csv

def compare_json(templatejson, comparejson, output_csv):
    # 读取JSON数据
    datatemplate = json.loads(templatejson)
    datacampare = json.loads(comparejson)

    # 获取所有键的集合
    all_keys = set(datatemplate.keys()).union(set(datacampare.keys()))

    # 创建CSV文件并写入标题行
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['allkey', '采控', '对比'])

        # 比较两个JSON的值并写入CSV文件
        for key in all_keys:
            value1 = datatemplate.get(key)
            value2 = datacampare.get(key)

            # if value1 != value2:
            writer.writerow([key, value1, value2])

    print("CSV文件生成成功！")

# 示例JSON数据
templatejson = '''
{
"bfdEnable":"",
"BGP_MD5":"",
"CE_AS":"4809",
"CE_IP":"172.18.0.90",
"CONNECT_TYPE_ID":"114094",
"customerName":"cust-psrtest0417",
"CVLAN_CODE":"2511",
"DETAIL_MODEL_CODE":"NE40E",
"deviceId":"222.173.0.203",
"DUALCIRCUIT_BEARING_MODE_ID":"主",
"exportRtName":"4809:5663100",
"extendInputParameter1":"",
"extendInputParameter2":"",
"HARDWARE_VERSION":"v5",
"importRTName":"4809:5663100",
"INTERFACE":"",
"IP":"172.18.",
"IPPrecedence":"",
"IPV4_ADDRESS":"172.18.0.89/30",
"IS_AS_OVERRIDE":"N",
"JOIN_CIRCUIT_CODE":"psrtest0407",
"MAX_PREFIX":"20",
"NET_TOPOLOGY_ID":"FullMesh",
"PE_AS":"64570",
"PORT_DESC":"For test148001084 20200709",
"PORT_NAME":"GigabitEthernet1/0/2",
"portMTU":"9178",
"qosBandwidth":"",
"qosBurstBandwidth":"",
"qosLevelId":"",
"qosOrderBandwidth":"",
"RATE_ID":"100503",
"rdName":"4809:56631",
"RESTART_TIME":"",
"ROUTE_PROTOCOL_ID":"102288",
"serviceGrades":"",
"sooEnable":"N",
"SVLAN_CODE":"2512",
"THRESHOLD":"",
"VENDOR":"华为",
"VPN_NO":"40001",
"VPN_SITE_ID":"济南",
"vrfName":"vrftest0522",
"WORK_MODE_ID":"全双工"
}
'''

comparejson = '''
{
 "VPN_SITE_ID":"null",
 "VPN_NO":"CTVPN35116",
 "DETAIL_MODEL_CODE":"371130000000000000000186",
 "importRTName":"4809:3511600",
 "WORK_MODE_ID":"null",
 "deviceId":"222.173.0.203",
 "portMTU":"1518",
 "IS_AS_OVERRIDE":"null",
 "bfdEnable":"null",
 "DUALCIRCUIT_BEARING_MODE_ID":"114154",
 "INTERFACE":"GigabitEthernet1/0/1.103",
 "sooEnable":"null",
 "SVLAN_CODE":"1004",
 "MAX_PREFIX":"2000.0",
 "PORT_NAME":"DEV0039l/GigabitEthernet1/0/1",
 "CVLAN_CODE":"null",
 "PORT_DESC":"",
 "exportRtName":"null",
 "IP":"null",
 "ROUTE_PROTOCOL_ID":"102288",
 "HARDWARE_VERSION":"",
 "RATE_ID":"100470",
 "NET_TOPOLOGY_ID":"null",
 "rdName":"4809:35116",
 "PE_AS":"4809",
 "CE_IP":"172.18.0.6",
 "CONNECT_TYPE_ID":"114094",
 "VENDOR":"华为",
 "JOIN_CIRCUIT_CODE":"济南CTVPN35116A",
 "BGP_MD5":"",
 "vrfName":"CTVPN35116-JTZQCRMCSZY",
 "IPV4_ADDRESS":"172.18.0.5",
 "CE_AS":"4809"
}
'''

# 指定输出的CSV文件路径
output_csv = "comparison_result.csv"

# 比较JSON并写入CSV
compare_json(templatejson, comparejson, output_csv)
