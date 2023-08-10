# -*- coding = utf-8 -*-
# @TIME :  10:39
# @Author : 晓晓鲸鱼
# @File : proxy_http.py
# @Software : PyCharm
# @脚本说明 : 代理模块，目前只支持HTTP协议

import random
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor
import threading

# 下面三行是可以禁用 非安全连接 提示
import urllib3
import warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)


class ProxyRequestHTTP:
    """
    请求发送模块
    支持代理和非代理模式
    """

    mode = ""  # 请求方式
    url = ""  # 请求地址
    proxy = ""  # 是否使用代理
    file = ""  # 数据包的路径
    data = ""  # post提交的数据

    ip_list = []  # 存放爬取下来的IP列表
    lock = threading.Lock()  # 线程锁
    pool = ThreadPoolExecutor(20)  # 扫描可用IP的线程池数量
    active_ip = []  # 存放可用IP的列表
    proxy_init_mode = False

    def __init__(self, url, mode, file="", data="", proxy=False, proxy_init=False):

        self.url = url
        self.mode = mode
        self.proxy = proxy
        self.file = file
        self.data = data
        self.proxy_init_mode = proxy_init

    def start(self):
        """
        :return: 请求的返回
        """

        if self.proxy:
            return self.__proxy(self.url)
        else:
            return self.__no_proxy(self.url)

    def init_proxy(self):
        """代理IP模块初始化"""

        # 初始化 - 模式置为True
        self.proxy_init_mode = True
        # 初始化 - 列表置空
        self.active_ip = []

        item = 1  # 要爬取的页数，从0开始，默认爬取10页IP，也就是100个

        while item < 4:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"
            }

            url = f'https://www.kuaidaili.com/free/intr/{item}/'
            item += 1

            proxy = {
                "http": "47.90.126.138:9090"
            }

            resp = requests.get(url, headers=headers, proxies=proxy)
            if resp.status_code == 200:
                # 初始化 - 清空IP文件
                with open("./proxy/proxy_active_ip.csv", "w") as f:
                    f.write("")

                # 提取IP的正则
                rule_get_ip = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                rule_get_port = r'<td data-title="PORT">(\d+)</td>'

                ip_addr = re.findall(rule_get_ip, resp.text)
                ip_port = re.findall(rule_get_port, resp.text)

                # 提取代理IP
                for i in range(0, 11):
                    self.ip_list.append(ip_addr[i] + ':' + ip_port[i])

            time.sleep(1)
        self.proxy_init_mode = False

        # todo
        print(self.ip_list)

        # 测试IP是否可用
        for ip in self.ip_list:
            self.pool.submit(self.check_proxy_ip, ip)
            # self.proxy_init_mode = False
        else:
            # self.proxy_init_mode = False
            pass

    def check_proxy_ip(self, ip):
        """测试代理IP是否可用"""

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"
        }
        proxy = {'http': ip}

        url = r"http://120.76.218.224/test/"  # 测试是否可用的IP

        try:
            resp = requests.get(url, headers=headers, timeout=10, proxies=proxy)

            self.lock.acquire()
            if url in resp.url:

                self.active_ip.append(ip)
                with open("./proxy/proxy_active_ip.csv", "a") as f:
                    f.write(ip + "\n")
                self.lock.release()

        except:
            pass

    def __no_proxy(self, url):
        """无代理模式"""

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }

        if self.mode == "get":
            return requests.get(url, verify=False, headers=headers)
        elif self.mode == "post":
            return requests.post(url, verify=False, headers=headers, data=self.data)

    def __proxy(self, url):
        """
        代理模式
        目前只支持HTTP的代理
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }

        # 如果没有重新加载代理IP，就使用文件里存储的IP
        # if not self.proxy_init_mode:
        if 1==2:
            with open("./proxy/proxy_active_ip.csv", "r") as f:
                self.active_ip = f.readlines()

        # 等待字典加载完毕
        if self.proxy_init_mode:
            # 等待列表中有IP后，再开始请求
            # if self.active_ip:

            # 随机排序IP，为了降低每次请求IP的重复度
            self.active_ip = random.sample(self.active_ip, k=len(self.active_ip))
            ip = self.active_ip.pop()

            proxy = {
                "http": ip.strip()
            }

            try:
                print(proxy)
                if self.mode == "get":
                    resp = requests.get(url, verify=False, headers=headers, proxies=proxy, timeout=3)
                elif self.mode == "post":
                    resp = requests.post(url, verify=False, headers=headers, data=self.data, proxies=proxy, timeout=3)
                if url in resp.url:
                    return resp
            except:
                pass


if __name__ == '__main__':

    data = {
        "name": "1123"
    }

    # a = ProxyRequestHTTP("http://120.76.218.224/test/test.php", mode="post", data=data, proxy=True)
    a = ProxyRequestHTTP("http://120.76.218.224/test", mode="get", proxy=True, proxy_init=True)
    a.init_proxy()
    resp_a = a.start()
    print(resp_a.url)
