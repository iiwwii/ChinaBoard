# -*- coding = utf-8 -*-
# @TIME :  21:08
# @Author : 晓晓鲸鱼
# @File : scan_ip.py
# @Software : PyCharm
# @脚本说明 :
import ipaddress
import socket
import threading
import ping3
import time
from multiprocessing import Lock


class SearchIp:

    def __init__(self):
        self.file_name_time = int(time.time())
        self.mutex = Lock()

    def __input_file(self, data):
        try:  # 文件不存在，创建文件并写入头行数据
            with open(f'./scan/scan_ip_{self.file_name_time}.csv', 'x', encoding='utf8') as f:
                f.write("ip\n")
        except FileExistsError:
            with open(f"./scan/scan_ip_{self.file_name_time}.csv", 'a', encoding="utf8") as f:
                f.write(f"{data}\n")

    def __search_ip(self, ip):
        # 等待时间为2s
        resp = ping3.ping(ip, timeout=2)
        if resp:
            self.mutex.acquire()
            print(f" [+]  {ip}  ")
            self.__input_file(ip)
            self.mutex.release()


    def start(self, ip_range):
        # ip对象
        ips = ipaddress.ip_network(ip_range).hosts()
        # 遍历ip
        start = time.time()
        for ip in ips:
            t = threading.Thread(target=self.__search_ip, args=(str(ip), ))
            t.start()
        t.join()
        end = time.time()
        print(f" [*]  扫描完毕 用时: {int(end-start)} s")


if __name__ == '__main__':
    # # 线程锁(限制12个线程)
    # pool_lock = threading.BoundedSemaphore(12)
    # user_input =
    # ips = ipaddress.ip_network(ip_range).hosts()

    # try:
    #
    #     a = SearchIp()
    #     start = time.time()
    #     a.start("192.168.11.0/24")
    #     end = time.time()
    #     print(end-start)
    # except:
    #     pass
    pass


