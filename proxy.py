# -*- coding = utf-8 -*-
# @TIME :  10:15
# @Author : 晓晓鲸鱼
# @File : proxy.py
# @Software : PyCharm
# @脚本说明 : 代理

import requests

# 下面三行是可以禁用 非安全连接 提示
import urllib3
import warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)


class Proxy:

    def __init__(self, url, mode="get", data="", headers=""):
        self.url = url
        self.mode = mode
        self.data = data
        self.headers = headers

    def start(self, https=False):

        # 自动判断是否为https
        url_head = self.url.split("://")[0]
        if "http" in url_head:
            https = True if url_head == "https" else False

        resp = self.__get_proxy_ip(https)
        if not resp == None:
            return resp
        else:
            self.__get_proxy_ip(https)

    def __get_proxy_ip(self, https):

        if https:
            url = "http://127.0.0.1:5010/get/?type=https"
        else:
            url = "http://127.0.0.1:5010/get/"

        # 获取代理IP
        resp_proxy = requests.get(url)
        resp_proxy_dirt = resp_proxy.json()

        # 获取代理的类型 http 或 https
        proxy_https_status = resp_proxy_dirt['https']
        # 获取代理IP
        proxy_ip = resp_proxy_dirt['proxy']

        # 判断获取到的代理是否为当前的代理模式 http 或 https
        if proxy_https_status == https:
            return self.__send_requests(proxy_ip, https)
        else:
            self.__get_proxy_ip(https)

    def __send_requests(self, proxy_ip, https):

        # 如果有传入header 则使用用户的，如果没有则使用自己的
        if self.headers:
            pass
        else:
            self.headers = {
                "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }

        # 写入不同模式的代理IP
        if https:
            proxy_dirt = {"https": f"https://{proxy_ip}"}
        else:
            proxy_dirt = {"http": f"http://{proxy_ip}"}

        # 发送代理请求
        try:
            if self.mode == "get":
                resp = requests.get(self.url, proxies=proxy_dirt, headers=self.headers, verify=False)
            elif self.mode == "post":
                resp = requests.post(self.url, data=self.data, proxies=proxy_dirt, headers=self.headers, verify=False)

            # 判断是否为目标网站返回的信息
            return resp if self.url in resp.url else self.__get_proxy_ip(https)

        except:
            self.__get_proxy_ip(https)  # 重发




if __name__ == '__main__':
    # url1 = "http://127.0.0.1:5010/get/?type=https"
    #
    # resp1 = requests.get(url1)
    #
    # print(resp1.text)
    # print(resp1.json()['https'])
    # print(resp1.json()['proxy'])

    option = Proxy("https://120.76.218.224/test/")
    resp = option.start(https=True)
    print(resp)
    print(resp.url)
    print(type(resp))

    # https = False
    #
    # if "False" == str(https):
    #     print(1)


