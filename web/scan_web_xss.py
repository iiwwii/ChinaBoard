#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：python_self 
@File    ：XSS扫描工具.py
@Author  ：CZ   
@Date    ：2023/6/29 14:08 
@脚本说明：XSS扫描工具
"""
import requests
# import 集成工具.proxy as proxy
import proxy


class ScanXss:

    # 类的基本属性
    def __init__(self, url, proxy_mode=False):
        self.url = url
        self.proxy_mode = proxy_mode

    def __str__(self):
        return "您输入的url地址是[%s],现在开始扫描" % self.url

    # 类方法
    # 从响应中检测payload是否有效
    def check_resp(self,response, payload, type):
        index = response.find(payload)
        # 前缀只要不是=号
        prefix = response[index - 2:index - 1]
        if type == 'Normal' and prefix != '=' and index >= 0:
            return True
        elif type == 'Prop' and prefix == '=' and index >= 0:
            return True
        elif index >= 0:
            return True
        return False


    def xss_get(self):
        # 拆分url地址为url和param参数部分
        # http://192.168.120.209/xss-labs-master/level2.php?keyword=test 具体url的形式
        url = self.url.split('?')[0]
        param = self.url.split('?')[1].split('=')[0]

        # 打开自己准备的的xss字典。
        # payload_list = file.readlines()：这行代码读取文件中的所有行，并将每一行的内容存储在payload_list列表中
        with open('./conf/xss_payload.txt') as file:
            payload_list = file.readlines()

        for payload in payload_list:
            # Normal:<script>alert(1)</script> payload的具体形式
            type = payload.strip().split(':', 1)[0]
            payload = payload.strip().split(':', 1)[1]
            if type == 'Referer' or type == 'User-Agent' or type == 'Cookie':
                header = {type: payload}

                if self.proxy_mode:
                    proxy_obj = proxy.Proxy(url=url, headers=header)
                    resp = proxy_obj.start()
                else:
                    resp = requests.get(url=url, headers=header)

            else:
                # data = {
                #     param: payload
                # }
                url = url + f"?{param}={payload}"
                if self.proxy_mode:
                    proxy_obj = proxy.Proxy(url=url)
                    resp = proxy_obj.start()
                else:
                    resp = requests.get(url=url)

            if self.check_resp(resp.text, payload, type):
                print(f"此处存在XSS漏洞{payload}")

    def xss_post(self, str):
        if '?' in self.url:
            post_url = self.url.split('?')[0]
        else:
            post_url = self.url
        with open('./conf/xss_post_payload.txt') as file:
            payload_list = file.readlines()

            for payload in payload_list:
                payload = payload.strip()
                post_list = str.split("&")
                post_dirt = {}

                for i in post_list:
                    # 写入字典
                    post_dirt[i.split("=", 1)[0]] = payload

                    if self.proxy_mode:
                        proxy_obj = proxy.Proxy(url=post_url, mode="post", data=post_dirt)
                        resp = proxy_obj.start()
                    else:
                        resp = requests.post(url=post_url, data=post_dirt)
                    sign = payload

                # 预防返回空字符串报错
                try:
                    if sign in resp.text:
                        print(f"[+]  有xss注入的漏洞，payload为{payload}")
                    else:
                        # print("[-]  没有xss的漏洞")
                        pass
                except:
                    pass


if __name__ == '__main__':

    my_scan = ScanXss('http://120.76.218.224/test/test.php', proxy_mode=True)
    my_scan.xss_post('name=1')
    # my_scan.XSS_scan()