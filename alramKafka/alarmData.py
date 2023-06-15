from dataclasses import dataclass,field

@dataclass
class alarmData:
    """Class for keeping track of an item in inventory."""
    alarmSeq: str #4389151
    alarmId: str  # 不为空 在专业综合网管内部要唯一)		4347359001
    alarmStatus: str# 1 0 1活动告警 0 清楚告警
    alarmTitle: str # 告警标题
    alarmSeverity: str # 不为空 1 2 3 4 取值
    eventTime: str # 告警时间
    alarmDes: str
    serviceIp: str = field(default="")
    relaIP: str = field(default="")
    locationInfo: str = field(default="")
    objectName: str = field(default="NE")
    msgType: str = field(default="alarm")  #alarm、heartbeat
    addInfo: str = field(default="")
    cityName: str = field(default="济南")
    areaName: str = field(default="")
    netLayer: str = field(default="")
    specialSubnet: str = field(default="")
    alarmReserved: str = field(default="")

# 心跳
@dataclass
class heartBeat:
    eventTime: str
    msgType: str = field(default="heartbeat")



# {
# "msgType":"heartbeat",
# "eventTime":"2021-01-15 16:03:00"
# }


# {
# "msgType":"alarm",
# "alarmSeq": "4389151",
# "alarmId": "4347359001",
# "alarmStatus": "1",
# "alarmTitle": "疑似国际话务盗拨-重要",
# "alarmSeverity": "1",
# "eventTime": "2022-05-16 08:11:14",
# "locationInfo": "主叫号码18905399108拨打国际号码[0088555819966,0088555819966888]23次,疑似国际话务盗拨",
# "objectName": "",
# "alarmDes": "2022-05-16 08:00:00~2022-05-16 08:10:00,主叫号码18905399108拨打国际号码[0088555819966,0088555819966888]23次,疑似国际话务盗拨",
# "addInfo": "",
# "cityName": "临沂",
# "areaName": "",
# "netLayer": "移动网软交换",
# "specialSubnet": "省网核心",
# "alarmReserved": ""
# }
