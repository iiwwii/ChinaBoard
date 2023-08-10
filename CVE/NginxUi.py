# -*- coding = utf-8 -*-
# @TIME :  11:49
# @Author : 晓晓鲸鱼
# @File : NginxUi.py
# @Software : PyCharm
# @脚本说明 :

import requests
import 集成工具.proxy as proxy
from concurrent.futures import ThreadPoolExecutor
import re



def check(url):

    proxy_obj = proxy.Proxy(url)
    resp = proxy_obj.start()

    if resp:
        pass









if __name__ == '__main__':

    pool = ThreadPoolExecutor(10)

