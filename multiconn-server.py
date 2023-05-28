# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : multiconn-server.py.py
# Time       ：2023/5/28 10:36
# Author     ：wwa
# version    ：python 3.11
# Description：
"""
import sys
# import socket
from collections import namedtuple
from socket import socket
from socket import AF_INET, SOCK_STREAM
import selectors  # 高级I/O复用
import types  # 动态创建类型
from typing import Union

sel = selectors.DefaultSelector()


def accept_wrapper(sock: socket) -> None:
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)  # 设置非阻塞
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # data = namedtuple(addr,"inb","outb",defaults=(b"",b""))
    events = selectors.EVENT_READ | selectors.EVENT_WRITE  # 注册事件
    # register(fileobj,events,data=None) fileobj 要监视的文件对象 events 要监视事件的位掩码 data是不透明对象
    # return  selectorKey实例
    sel.register(conn, events, data=data)


def service_connection(key: selectors.SelectorKey, mask: Union[selectors.EVENT_READ, selectors.EVENT_WRITE]) -> None:
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echong {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print(f"Usage: sys.argv[0] <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket(AF_INET, SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)

except KeyboardInterrupt:
    # 房间里面的大象
    print("Caught keyboard interrupt ,exiting")
finally:
    sel.close()
