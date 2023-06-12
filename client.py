# coding:utf-8

import socket

# 创建一个socket对象
obj = socket.socket()

# 连接服务端ip和端口
obj.connect(('127.0.0.1',6053,))
# 阻塞
ret_bytes = obj.recv(1024)
# 转成str
ret_str = str(ret_bytes,encoding='utf-8')
# 输出
print(ret_str)

while True:
    # 进入连接 用户输入内容
    inp = input("Client请输入要发送的内容>>>>")
    # q
    if inp == 'q':
        obj.sendall(bytes(inp,encoding='utf-8'))
        break
    else:
        # 否则把用户输入的内容发送给用户
        obj.sendall(bytes(inp,encoding='utf-8'))
        # 等待服务器回答
        print("正在等待Server输入内容....")
        # 获取服务端发送过类的结果
        ret = str(obj.recv(1024),encoding="utf-8")
        # 输出结果
        print(ret)
# 连接完成之后关闭链接
obj.close()