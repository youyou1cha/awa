# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : multiconn-client.py.py
# Time       ：2023/5/28 11:31
# Author     ：wwa
# version    ：python 3.11
# Description：
"""

import sys
import socket
import selectors
import types
from typing import Union

sel = selectors.DefaultSelector()
messages = [b"message 1 from client", b"message 2 fom client."]


def start_connections(host: str, port: int, num_conns: int) -> None:
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connections {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)


def service_connection(key: selectors.SelectorKey, mask: Union[selectors.EVENT_READ, selectors.EVENT_WRITE]) -> None:
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(f"Recevied {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    if mask * selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


if len(sys.argv) != 4:
    print(f"Usage:{sys.argv[0]} <host> <port> <num_connection>")
    sys.exit(1)
host, port, num_conns = sys.argv[1:4]

start_connections(host, int(port), int(num_conns))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key,mask in events:
                service_connection(key,mask)
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caughtn keyboard interrput exiting")
finally:
    sel.close()
