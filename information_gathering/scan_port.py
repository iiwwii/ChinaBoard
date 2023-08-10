# -*- coding = utf-8 -*-
# @TIME :  22:56
# @Author : 晓晓鲸鱼
# @File : 面向对象_多线程_端口扫描.py
# @Software : PyCharm
# @脚本说明 :


import socket
import threading
import time
from ping3 import ping
import ipaddress
import multiprocessing

from colorama import init, Fore, Style, Back
init(autoreset=True, convert=True)  # 确保控制台输出彩色

class SearchPort:

    def __init__(self, ip, lock, min_p=0, max_p=0):
        self.ip = ip
        self.min_p = min_p
        self.max_p = max_p
        self.file_name_time = int(time.time())
        # self.mutex1 = threading.Lock()

    def __input_file(self, data):
        try:  # 文件不存在，创建文件并写入头行数据
            with open(f'./scan/scan_port_{self.file_name_time}.csv', 'x', encoding='utf8') as f:
                f.write("ip,port,server\n")
        except FileExistsError:
            with open(f"./scan/scan_port_{self.file_name_time}.csv", 'a', encoding="utf8") as f:
                f.write(f"{data}\n")

    # 扫描端口
    def __search_port(self, ip, port):
        search = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        search.settimeout(2)
        rep_status = search.connect_ex((ip, port))
        if rep_status == 0:
            # print(f" {Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}]{Style.RESET_ALL} {ip} >>> {port}")
            # self.mutex1.acquire()
            print(f" [+]  {ip} >>> {port}")
            self.__input_file(f"{ip},{port},''")
            # self.mutex1.release()
            search.close()

    def __search_important_port(self, ip, port, server):
        search = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        search.settimeout(2)
        rep_status = search.connect_ex((ip, port))
        if rep_status == 0:
            # print(f"{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}]{Style.RESET_ALL} {ip} >>> {port} > {server}  ")
            # self.mutex1.acquire()
            print(f" [+]  {ip} >>> {port} > {server}  ")
            self.__input_file(f"{ip},{port},{server}")
            search.close()
            # self.mutex1.release()

    def __search_ip_important_port(self, ip):
        list_port = {7: 'echo', 21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp', 43: 'whois', 53: 'domain name system (DNS)',
                     67: 'bootps', 68: 'bootpc', 69: 'tftp', 79: 'finger', 80: 'http', 81: 'http', 88: 'kerberos',
                     109: 'pop2', 110: 'pop3', 113: 'ident', 119: 'nntp', 123: 'ntp', 135: 'RPC', 137: 'NetBIOS',
                     138: 'NetBIOS', 139: 'NetBIOS', 143: 'imap', 161: 'SNMP', 162: 'SNMP', 179: 'BGP', 194: 'IRC',
                     220: 'IMAP3', 389: 'LDAP', 443: 'https', 445: 'SMB', 465: 'SMTPS', 513: 'rlogin', 520: 'RIP',
                     546: 'DHCPv6', 547: 'DHCPv6', 554: 'RTSP', 563: 'NNTPS', 631: 'IPP', 636: 'LDAP', 991: 'Netnews',
                     993: 'IMAPS', 995: 'POP3S', 1080: 'SOCKS', 1194: 'OpenVPN', 1433: 'Microsoft SQL Server',
                     1434: 'Microsoft SQL Monitor', 1494: 'Citrix Independent Computing Architecture', 1521: 'Oracle database',
                     1701: 'L2TP', 1723: 'PPTP', 1755: 'Microsoft Media Services (MMS)', 1812: 'RADIUS', 1813: 'RADIUS',
                     1863: 'MSN', 3269: 'Microsoft Active Directory', 3306: 'MySQL', 3307: 'MySQL', 3389: 'Remote Desktop Protocol (RDP)',
                     3544: 'Teredo', 4369: 'Erlang Port Mapper', 5060: 'SIP', 5061: 'SIP over TLS', 5355: 'LLMNR', 5432: 'PostgreSQL',
                     5671: 'AMQP', 5672: 'AMQP', 6379: 'redis_server', 7001: 'redis_server', 8080: 'http', 8081: 'http', 8088: 'http', 8443: 'https',
                     8883: 'MQTT', 8888: 'http', 9443: 'https', 9988: 'http', 15672: 'RabbitMQ Management', 50389: 'Windows Management Instrumentation (WMI)',
                     50636: 'Windows Communication Foundation (WCF)', 61613: 'STOMP', 61614: 'STOMP over SSL/TLS'}
        resp = ping(ip, timeout=2)
        if resp:
            for port in list_port:
                # 拿到端口对应的服务名称
                server = list_port[port]
                t_port = threading.Thread(target=self.__search_important_port, args=(ip, port, server))
                t_port.start()

    # 扫描IP，并多线程扫描端口
    def __search_ip(self, ip):
        resp = ping(ip)
        if resp:
            for port in range(self.min_p, self.max_p + 1):
                t_port = threading.Thread(target=self.__search_port, args=(ip, port))
                t_port.start()

    # 组合IP，并多线程扫描IP
    def start(self, ip_addr, mode):
        if mode == "1":
            t_ip = threading.Thread(target=self.__search_ip, args=(f"{ip_addr}",))
            t_ip.start()

        elif mode == "2":
            t_ip = threading.Thread(target=self.__search_ip_important_port, args=(f"{ip_addr}",))
            t_ip.start()


if __name__ == '__main__':
    user_ip = input("IP范围 >>> ")
    user_mode = input("1.自定义端口,2.常见端口 >>> ")

    if user_mode == "1":
        user_min_p = int(input("最小端口 >>> "))
        user_max_p = int(input("最大端口 >>> "))
        a = SearchPort(user_ip, min_p=user_min_p, max_p=user_max_p)
    elif user_mode == "2":
        a = SearchPort(user_ip)

    # ip列表
    ip_list = ipaddress.ip_network(user_ip)

    # 进程池数量  根据当前电脑CPU进程调整
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    start = time.time()
    for addr in ip_list.hosts():
        pool.apply_async(func=a.start, args=(str(addr), user_mode))

    pool.close()
    pool.join()

    end = time.time()
    print("扫描完毕，用时: " + str(int(end - start)) + " s")
