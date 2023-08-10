
import requests
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor, wait
import re
import proxy   # 这里报错没事，这里写的是导入该文件后的路径
import time


# 递归扫描网页第一层目录
class GetDirLink:

    # 存放本站的地址，如 https://www.baidu.com
    web_site = ""
    # 存放已经扫描过的URL
    scanned_url_list = []
    # 存放是否开关代理
    proxy = ""
    # 线程锁
    lock = threading.Lock()
    filename = ""

    def __init__(self, thread_pool=5):

        # # 创建线程锁
        # self.lock = threading.Lock()
        # 线程池,默认数量为5
        self.thread_pool = ThreadPoolExecutor(thread_pool)

    def start(self, url, proxy=False):
        self.web_site = url.strip("/")  # 去除网站末尾的"/"
        self.proxy = proxy
        # 创建文件名
        self.filename = f"scan_dir_{url.split('://', 1)[1]}_{int(time.time())}.csv"

        self.get_url(self.web_site)

    def get_url(self, url):
        """请求URL，获取网页，进而获取A标签"""

        self.lock.acquire()
        print(url)
        self.lock.release()

        if self.proxy:
            https_mode_user = self.web_site.split("://", 1)[0]   # 提取最前端的模式, http 或https
            https_mode = True if https_mode_user == "https" else False
            # 请求代理
            proxy_mode = proxy.Proxy(url)
            resp = proxy_mode.start(https=https_mode)
        else:
            resp = requests.get(url, timeout=3)

        self.get_a_tag(resp.text)

    def get_a_tag(self, text):
        """获取A标签"""

        # 匹配是否为URL或URI地址的规则
        re_rule_check_http = r"^((http|https)://)"
        re_rule_check_uri = r"^/.+"

        # 提取网页所有A标签
        soup = BeautifulSoup(text, 'html.parser')
        a_tags = soup.find_all('a')

        # 遍历所有A标签，并判断标签是否属于本站
        for a_tag in a_tags:
            # 提取标签中的链接
            link = a_tag.get('href')
            if link:
                # 判断是否为HTTP网页
                re_resp_check_http = re.search(re_rule_check_http, link)
                if re_resp_check_http:
                    self.thread_pool.submit(self.check_url, link)

                # 判断是否为uri路径，如果是则拼接URL
                re_resp_check_uri = re.search(re_rule_check_uri, link)
                if re_resp_check_uri:
                    # 拼接URL
                    link = self.web_site + link
                    self.thread_pool.submit(self.check_url, link)
                    # wait([a])

    def check_url(self, url):
        """判断URL是否为本网站"""

        # 规则: 判断是否为本站的URL
        re_rule_check_this_site = rf"^({self.web_site})"
        # 规则: 判断是否为 一层 目录
        re_rule_check_one_layer = r"^(http|https)://[^/]+?/[^/]+/?$"

        # 判断是否为本站URL
        re_resp_check_this_site = re.search(re_rule_check_this_site, url)
        if re_resp_check_this_site:
            # 判断是否为一层目录
            re_resp_check_one_layer = re.search(re_rule_check_one_layer, url)
            if re_resp_check_one_layer:
                # 判断是否已经扫描过
                # self.lock.acquire()
                if url not in self.scanned_url_list:
                    # print(url)
                    # self.lock.release()
                    self.scanned_url_list.append(url)
                    self.get_url(url)

    def __del__(self):
        """写文件"""
        with open(f"./scan/{self.filename}", mode="a", encoding="utf8") as file:
            for site in self.scanned_url_list:
                file.write(f"{site}\n")


if __name__ == '__main__':
    a = GetDirLink()
    a.start("https://www.kuaidaili.com/")
