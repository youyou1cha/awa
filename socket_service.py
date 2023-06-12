# coding:utf-8
import socket

# 创建一个socket对象
sk = socket.socket()
# 允许
sk.bind(('127.0.0.1',6542))
# 最大连接数
sk.listen(5)

# 
while True:
    conn,address = sk.accept()

    # 客户端发送过来的文件大小
    file_size = str(conn.recv(1024),encoding="utf-8")

    # 告诉客户端
    conn.sendall(bytes("ack",encoding="utf-8"))

    # 文件大小转换成int类型
    total_size = int(file_size)

    # 创建一个默认的值
    has_recv = 0

    # 打开新文件
    f = open("new_file.txt",'wb')

    while True:
        if total_size == has_recv:
            break

        # 接入客户端发送过来内容
        data = conn.recv(1024)
        f.write(data)
        has_recv += len(data)
    f.close()