# coding:utf-8

import socket

obj = socket.socket()

obj.connect(('127.0.0.1',999,))

ret_bytes = obj.recv(1024)

ret_str = str(ret_bytes,encoding='utf-8')

print(ret_str)

while True:
    inp = input("client请输入发送内容>>>")
    if inp == 'q':
        obj.sendall(bytes(inp,encoding='utf-8'))
        break
    else:
        obj.sendall(bytes(inp,encoding='utf-8'))
        print("正在等待server输入内容....")
        ret = str(obj.recv(1024),encoding='utf-8')
        print(ret)
obj.close()