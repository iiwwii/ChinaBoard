#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject1 
@File    ：scan.py.py
@Author  ：林香
@Date    ：2023/7/13 16:05 
@脚本说明：
"""
import requests
import urllib3
import warnings
import time
import proxy

warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
from concurrent.futures import ThreadPoolExecutor


class SubdomainScanner:

    proxy = ""

    def __init__(self, protocol, url, sublist):
        self.protocol = protocol
        self.url = url
        self.sublist = sublist
        self.filename = f"scan_sub_{url}_{int(time.time())}.csv"

    # 静态方法，可以在没有类实例的情况下调用它
    @staticmethod
    def loadfile(filepath):
        result = []
        with open(filepath, 'r') as f:
            for line in f:
                result.append(line.strip())
        return result

    def check_url(self, sub):
        # 拼接子域名
        suburl = self.protocol + "://" + sub + "." + self.url
        # print(suburl)
        try:
            # 测试子域名是否存在

            if self.proxy:
                proxy_obj = proxy.Proxy(suburl)             # 创建代理对象
                proxy_https = suburl.split("://", 1)[0]     # 分割，提取 http 或 https
                proxy_https_mode = True if proxy_https == "https" else False    # 判断是否为 https
                urlres = proxy_obj.start(https=proxy_https_mode)        # 发送代理请求
            else:
                urlres = requests.get(suburl, timeout=5, verify=False)

            if urlres.status_code == 200 or urlres.status_code == 403:
                print("[+]  {} status -> {}".format(suburl, urlres.status_code))
                with open(f"./scan/{self.filename}", "a", encoding="utf-8") as f:
                    f.write(f"{suburl},{urlres.status_code}\n")
        except:
            pass

    def scan(self, proxy):

        self.proxy = proxy

        with ThreadPoolExecutor(max_workers=5) as executor:
            # 遍历子域名列表，将每个子域名提交给线程池处理
            for sub in self.sublist:
                executor.submit(self.check_url, sub)


def main(url, proxy=False):

    list = url.split("://", 1)
    protocol = list[0]   # 提取最开头的协议
    url = list[1]

    sublist = SubdomainScanner.loadfile("./conf/sub.txt")
    scanner = SubdomainScanner(protocol, url, sublist)
    scanner.scan(proxy)


if __name__ == '__main__':
    main("https://woniuxy.com")
