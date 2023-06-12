# coding:utf-8

import socket
import os

# 创建一个socket对象
obj = socket.socket()
# 服务端IP和端口
obj.connect(('127.0.0.1',6542))
# os获取文件总大小
size = os.stat('old_file.txt').st_size
# 把文件总大小发送给服务端
obj.sendall(bytes(str(size),encoding='utf-8'))
# 接受服务端返回的信息
obj.recv(1024)
# 以rb模式打开一个要发送的文件d
with open("old_file.tx","rb") as f:
    # 循环文件的所有内容
    for line in f:
        obj.sendall(line)
obj.close()