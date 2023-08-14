import json
import csv
import re
import json


def remove_comments(json_text):
    # 正则表达式匹配 "//" 注释，并将其替换为空字符串
    cleaned_text = re.sub(r'//.*', '', json_text)
    # 正则表达式匹配行内注释，并将其替换为空字符串
    cleaned_text = re.sub(r'/\*.*?\*/', '', cleaned_text, flags=re.DOTALL)
    return cleaned_text


# 两端文本
text1 = """
{
    "testname":"CX600ASBR",
	"deviceId": "150.139.0.179",
	"deviceIp": "150.139.0.179",
	"acPort": "GigabitEthernet1/1/1",
    "vlanType": "dot1q",  // 
	"acPortVlan": "1605",  // 
	"qosSpeedTemplateName": "10M",
	"qosCir": "20000",
	"qosPir": "20000",
	"serviceSpeed": "100408",
	"direction": "",  //
	"portDesc": "psrtest03241", 
	"ipv4Mtu": "2000",
	"acName": "",
	"pwClassName": "",
	"mBFDName": "",
	"sBFDName": "",
	"bfdSessionName1": "",
	"bfdSessionName2": "",
	"bfdDiscriminator1": "",
	"bfdDiscriminator2": "",
	"pwOutLabel1": "",
	"pwInLabel1": "",
	"pwOutLabel2": "",
	"pwInLabel2": "",
	"tunnelId1": "",
	"tunnelId2": "",
	"mVcid": "810201",  //
	"sVcid": "810202",  // 
	"vpwsName": "",
	"flowPointId": "",
	"connPort1": "",
	"connPortVlan1": "",
	"connPort2": "",
	"connPortVlan2": "",
	"connPortIp1": "",
	"connPortIp2": "",
	"mPWName": "",
	"sPWName": "",
	"cipName": "",
	"timeInterval": "",
	"timeMultiplier": "",
	"apsProtectGroupName": "",
	"pwgInstanceName": "",
	"proSwitchId": "",
	"downServiceIp1": "",  // B1
	"upServiceIp1": "150.139.0.143",              
	"downServiceIp2": "",  // B2
	"upServiceIp2": "150.139.0.144",            
	"extendInputParameterA": "",
	"extendInputParameterB": "",
	"TASKTYPE": "viewconfiglet"
}
"""

text2 = """
{
	"sBFDName":"null",
	"null":"null",
	"deviceIp":"150.139.0.179",
	"apsProtectGroupName":null,
	"deviceId":"150.139.0.179",
	"mBFDName":"null",
	"proSwitchId":null,
	"connPortVlan1":"1215",
	"connPortVlan2":null,
	"connPortIp2":null,
	"tunnelOutLabel":"null",
	"connPortIp1":"",
	"tunnelInLabe2":"null",
	"vlanType":"dot1q",
	"mtuTemplateName":null,
	"pwMode":null,
	"deviceType":"",
	"tunnelId2":"null",
	"pwInLabel1":"null",
	"tunnelId1":"null",
	"pwInLabel2":"null",
	"pwOutLabel2":"null",
	"pwOutLabel1":"null",
	"mPWName":"null",
	"bfdSessionName2":"",
	"bfdSessionName1":"",
	"ipv4Mtu":"2000",
	"upServiceIp1":"null",
	"extendInputParameterB":"100002386015",
	"upServiceIp2":"null",
	"extendInputParameterA":"济南CTVPN35130B",
	"remoteConnPort1":"",
	"l3ProfileName2":null,
	"remoteConnPort2":null,
	"l3ProfileName1":null,
	"deviceClass":"STN-ASBR",
	"sPWName":"null",
	"timeMultiplier":null,
	"lspName2":"null",
	"mVcid":"810272",
	"lspName1":"null",
	"pwgInstanceName":null,
	"bfdDiscriminator2":null,
	"remoteConnPortVlan2":null,
	"bfdDiscriminator1":null,
	"remoteConnPortVlan1":"1215",
	"remoteConnPortIp1":null,
	"remoteConnPortIp2":null,
	"tunnelOutLabe2":"null",
	"vpwsName":"810272",
	"portDesc":"济南CTVPN35130B",
	"pwClassName":null,
	"connPort2":null,
	"qosCir":null,
	"connPort1":"GigabitEthernet1/1/1",
	"acName":null,
	"acPortVlan":"1215",
	"serviceSpeed":"null",
	"timeInterval":"",
	"acPort":"GigabitEthernet1/1/1",
	"tunnelInLabel":"null",
	"direction":"",
	"qosPir":"",
	"sVcid":"",
	"tunnelPortName2":"null",
	"tunnelPortName1":"null",
	"deviceVersion":"",
	"qosSpeedTemplateName":null,
	"deviceVender":"",
	"cipName":"null",
	"flowPointId":""
}
"""

import json
import csv


def text_to_json(text):
    # 将文本转换为JSON格式
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误：{e}")
        return None


def compare_jsons(json1, json2):
    # 对比两个JSON并找出差异
    common_keys = set(json1.keys()) & set(json2.keys())
    only_json1_keys = set(json1.keys()) - set(json2.keys())
    only_json2_keys = set(json2.keys()) - set(json1.keys())
    diff = {
        'Common': {},
        'Only in JSON1': {},
        'Only in JSON2': {}
    }

    # 处理相同的键值对
    for key in common_keys:
        # if json1[key] != json2[key]:
        diff['Common'][key] = {
            'original_value': json1[key],
            'new_value': json2[key],
        }

    # 处理只存在于JSON1的键值对
    for key in only_json1_keys:
        diff['Only in JSON1'][key] = {
            'original_value': json1[key],
            'new_value': 'Key not found in JSON2',
        }

    # 处理只存在于JSON2的键值对
    for key in only_json2_keys:
        diff['Only in JSON2'][key] = {
            'original_value': 'Key not found in JSON1',
            'new_value': json2[key],
        }

    return diff


def generate_csv(diff, output_file):
    # 将差异生成为CSV文件
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Type', 'Key', 'Original Value', 'New Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for type_, keys in diff.items():
            for key, values in keys.items():
                writer.writerow({
                    'Type': type_,
                    'Key': key,
                    'Original Value': values['original_value'],
                    'New Value': values['new_value'],
                })


if __name__ == "__main__":
    # 假设您有两个文本变量：text1和text2，表示两端文本
    # text1 = '{"name": "Alice", "age": 30, "city": "New York"}'
    # text2 = '{"name": "Bob", "city": "San Francisco", "hobbies": ["reading", "painting"]}'

    cleaned_json1 = remove_comments(text1)
    cleaned_json2 = remove_comments(text2)

    # 将文本转换为JSON
    json1 = text_to_json(cleaned_json1)
    json2 = text_to_json(cleaned_json2)

    print(json1)
    print(json2)

    if json1 is not None and json2 is not None:
        # 对比两个JSON并找出差异
        diff = compare_jsons(json1, json2)

        # 将差异生成为CSV文件
        output_file = 'json_diff.csv'
        generate_csv(diff, output_file)
        print(f"CSV文件已生成: {output_file}")
