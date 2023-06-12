# coding:utf-8

import socketserver

class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request

        conn.sendall(bytes("i你好 huan ",encoding='utf-8'))

        while True:
            print("正在等待client输入内容")
            ret_bytes = conn.recv(1024)
            ret_str = str(ret_bytes,encoding='utf-8')

            print(ret_str)

            if ret_str == 'q':
                break

            inp = input('service 请输入要发送的内容>>>')
            conn.sendall(bytes(inp,encoding='utf-8'))

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',999,),MyServer)
    server.serve_forever()