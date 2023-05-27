import socket
import struct
import telnetlib
from concurrent.futures import ThreadPoolExecutor
# import paramiko
# import socket

def ping_ip(ip):
    """
    测试ICMP ping命令是否能够ping通IP地址
    """
    try:
        icmp = socket.getprotobyname("icmp")
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        sock.settimeout(2)
        # 构建ICMP请求报文
        packet_id = int((id(sock) % 65535))
        packet_data = b'Hello World'
        packet_checksum = 0
        header = struct.pack("bbHHh", 8, 0, packet_checksum, packet_id, 1)
        packet_checksum = checksum(header + packet_data)
        header = struct.pack("bbHHh", 8, 0, packet_checksum, packet_id, 1)
        # 发送ICMP请求报文
        sock.sendto(header + packet_data, (ip, 1))
        # 接收ICMP回复报文
        response, addr = sock.recvfrom(1024)
        icmp_type, code, checksum, packet_id, sequence = struct.unpack("bbHHh", response[20:28])
        if icmp_type == 0:
            return '{} ping success'.format(ip)
        else:
            return '{} ping fail'.format(ip)
    except:
        return '{} ping fail'.format(ip)



# def ssh_connect(ip, username, password):
#     try:
#         ssh_client = paramiko.SSHClient()
#         ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh_client.connect(ip, username=username, password=password, timeout=5)
#         ssh_client.close()
#         return '{} ssh success'.format(ip)
#     except:
#         return '{} ssh fail'.format(ip)


def ssh_connect(ip, username, password):
    # 创建一个TCP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置连接超时时间为5秒
    sock.settimeout(5)
    try:
        # 连接SSH服务器的22端口
        sock.connect((ip, 22))
        # 接收服务器发送的数据
        banner = sock.recv(1024)
        if banner.startswith(b'SSH'):
            # 发送用户名和密码进行认证
            sock.sendall(username.encode('utf-8') + b'\r\n')
            sock.sendall(password.encode('utf-8') + b'\r\n')
            # 接收认证结果
            result = sock.recv(1024)
            if b'Access denied' not in result:
                sock.close()
                return '{} ssh success'.format(ip)
        sock.close()
        return '{} ssh fail'.format(ip)
    except:
        sock.close()
        return '{} ssh fail'.format(ip)

def telnet_ip(ip, username, password):
    """
    测试telnet是否能够连通IP地址，并使用给定的用户名和密码进行认证
    """
    try:
        telnetlib.Telnet(ip, timeout=2)
        tn = telnetlib.Telnet(ip)
        # tn.read_until(b"login: ")
        tn.write(username.encode('ascii') + b"\n")
        # tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        # tn.read_until(b"$")
        # tn.write(b"exit\n")
        return '{} telnet success'.format(ip)
    except:
        return '{} telnet fail'.format(ip)


def checksum(data):
    """
    计算ICMP报文的校验和
    """
    if len(data) % 2:
        data += b'\x00'
    res = sum(struct.unpack('!%sH' % (len(data) // 2), data))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return (~res) & 0xffff


def test_ip(ip, protocol, username, password):
    """
    测试IP地址的ping和telnet连通性，并将结果保存在txt文件中
    """

    if protocol == 'ping':
        res = ping_ip(ip)
        with open('test_result.txt', 'a') as f:
            f.write(f'{ip}\t{res}\n')
        print(f'{ip}\t{res}\n')
    elif protocol == 'telnet':
        res = telnet_ip(ip,username,password)
        with open('test_result.txt', 'a') as f:
            f.write(f'{ip}\t{res}\n')
        print(f'{ip}\t{res}\n')
    elif protocol == 'ssh':
        res = ssh_connect(ip, username, password)
        with open('test_result.txt', 'a') as f:
            f.write(f'{ip}\t{res}\n')
        print(f'{ip}\t{res}\n')
    else:
        return False

if __name__ == '__main__':
    # 创建一个线程池，最大线程数为10
    executor = ThreadPoolExecutor(max_workers=100)
    # 读取IP列表，将每个IP提交给线程池处理
    with open('ip_list.txt', 'r') as f:
        for line in f:
            ip, protocol, username, password = line.strip().split('\t')
            executor.submit(test_ip, ip, protocol, username, password)

    # 关闭线程池，等待所有任务完成
    executor.shutdown(wait=True)
