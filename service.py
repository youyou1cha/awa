# coding:utf-8
import socket
# 创建一个socket对象
sk = socket.socket()

# 绑定允许连接的IP地址和端口
sk.bind(('127.0.0.1',6053,))

# 服务端允许起来之后，限制客户端的连接数量
sk.listen(5)

while True:
    # 阻塞 等待接收客户端的请求。如果客户端连接会获取两个值，conn创建的连接 address=客户端的ip和端口
    conn,address = sk.accept()

    # 当用户连接的时候就给发送一条信息。python3里面需要发送内容的字节
    conn.sendall(bytes("i你好，欢迎登录！",encoding="utf-8"))

    # 
    while True:
        # 输出等待客户端发送内容
        print("正则等待Client输入内容.....")
        # 接入客户端发送过来
        ret_bytes = conn.recv(1024)
        # 转换成字符串类型
        ret_bytes = str(ret_bytes,encoding='utf-8')
        # 输出用户发送过来的内容
        print(ret_bytes)

        # 判断
        if ret_bytes == "q":
            break

        inp = input("Service请输入要发送的内容>>>")
        conn.sendall(bytes(inp,encoding='utf-8'))