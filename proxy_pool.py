# -*- coding = utf-8 -*-
# @TIME :  10:50
# @Author : 晓晓鲸鱼
# @File : proxy_pool.py
# @Software : PyCharm
# @脚本说明 :
import os
import socket
import subprocess
import time

import requests
import platform
from necessary_environment import proxy_pool, redis_server


class ProxyPool:

    system = ""
    redis = ""  # 存放redis启动的对象
    proxy_schedule = ""
    proxy_api = ""

    def __init__(self):
        self.system = platform.system()     # 检测当前操作系统类型
        # 用于检测服务是否启动，通过端口检测
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        # 检测Redis状态
        self.__redis_check(sock)
        # 检测代理池状态
        self.__proxy_check(sock)

    def __redis_check(self, sock):
        """目前只支持windows自启动，linux需手动开启redis"""

        resp_redis_status = sock.connect_ex(('localhost', 6379))    # 检测Reids是否开放
        if resp_redis_status == 0:
            print("[+]  Redis 启动成功")
            return True
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            if self.system == "Windows":
                # 拼接程序路径
                redis_server_dir = os.path.join(script_dir, "necessary_environment", "redis_server", "redis-server.exe")
                # 启动Redis
                # self.redis = subprocess.Popen(redis_server_dir, stdout=False, stderr=False)
                self.redis = subprocess.Popen(redis_server_dir, creationflags=subprocess.CREATE_NEW_CONSOLE)
                # time.sleep(3)


    def __proxy_check(self, sock):
        """检测代理池是否运行"""

        resp_proxy_status = sock.connect_ex(('localhost', 5010))
        if resp_proxy_status == 0:
            print("[+]  代理池启动成功")
            return True
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            if self.system == "Windows":
                proxy_server_dir = os.path.join(script_dir, "necessary_environment", "proxy_pool", "proxyPool.py")
                # proxy_server_dir = os.path.join(script_dir, "necessary_environment", "proxy_pool", "fuck.bat")
                proxy_api_cmd = f"pythonw {proxy_server_dir} server"
                proxy_schedule_cmd = f"pythonw {proxy_server_dir} schedule"
                # 启动代理池的调度服务
                self.proxy_schedule = subprocess.Popen(["python", proxy_server_dir, "server"], creationflags=subprocess.CREATE_NEW_CONSOLE)
                # 启动代理池API服务
                self.proxy_api = subprocess.Popen(["python", proxy_server_dir, "schedule"], creationflags=subprocess.CREATE_NEW_CONSOLE)


    def __del__(self):
        # input()
        # 程序结束后，关闭打开的服务
        self.redis.terminate()
        self.proxy_api.terminate()
        self.proxy_schedule.terminate()


if __name__ == '__main__':
    # print(platform.system())
    # while True:
    a = ProxyPool()
    while True:
        option = input(" - Q键退出 - ")
        if option == "q":
            break

