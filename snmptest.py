import subprocess
import sys

def p(Result):
    sys.stdout.write(Result + "\n")
    sys.stdout.flush()
def w(Result):
    with open("ipran_ping_snmp.txt") as f:
        f.writelines(Result)
with open('ipran.txt', 'r') as file:
    for line in file:
        ip, community = line.strip().split("===")

        # 进行Ping测试
        ping_command = f"ping -c 1 {ip}"
        ping_process = subprocess.Popen(ping_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ping_output, _ = ping_process.communicate()

        # 解析Ping结果
        ping_result = "ok" if ping_process.returncode == 0 else "fail"

        # 打印Ping结果
        # print(f"{ip} Ping result: {ping_result}")
        echo = f"{ip} Ping result: {ping_result}"
        p(echo)
        w(echo)

        # 转义特殊字符
        community_escaped = community.replace("'", "'\\''")

        # 构建命令
        snmpwalk_command = f"timeout 1 snmpwalk -v2c -c '{community_escaped}' {ip} sysName"
        print(snmpwalk_command)
        # 执行命令并获取结果
        try:
            snmpwalk_output = subprocess.check_output(snmpwalk_command, shell=True, stderr=subprocess.STDOUT,
                                                     universal_newlines=True)
            # print(f"{ip} SNMP walk successful")
            echo = f"{ip} SNMP walk successful"
            p(echo)
            w(echo)

        except subprocess.CalledProcessError as e:
            # print(f"{ip} SNMP walk failed: {e.output.strip()}")
            echo = f"{ip} SNMP walk failed: {e.output.strip()}"
            p(echo)
            w(echo)
        # print("-------------------")
        
