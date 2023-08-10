# -*- coding = utf-8 -*-
# @TIME :  17:31
# @Author : 晓晓鲸鱼
# @File : scan_ subdomain.py
# @Software : PyCharm
# @脚本说明 :
import multiprocessing
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
import keyboard
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)     # 禁用安全警告
import time


class ScanSubdomain:

    def __init__(self, thr_num):
        self.pool = ThreadPoolExecutor(max_workers=thr_num)     # 线程数量
        # self.pool_lock = threading.BoundedSemaphore(thr_num)
        self.running = True     # 判断程序是否结束的条件
        self.num = 0            # 计数
        self.file_name_time = int(time.time())
        self.mutex = multiprocessing.Lock()

    def __input_file(self, data):
        try:  # 文件不存在，创建文件并写入头行数据
            with open(f'./scan/scan_web_{self.file_name_time}.csv', 'x', encoding='utf8') as f:
                f.write("site,code\n")
        except FileExistsError:
            with open(f"./scan/scan_web_{self.file_name_time}.csv", 'a', encoding="utf8") as f:
                f.write(f"{data}\n")

    def __scan_sub(self, url):
        # self.pool_lock.acquire()
        if self.running:    # 判断是否退出
            try:
                resp = requests.get(url, verify=False, timeout=2)  # 关闭HTTPS证书认证
                resp_code = resp.status_code
                if resp_code in (200, 301, 302, 403):
                    self.mutex.acquire()
                    print("")
                    print(f" [+]  {url} >>> {resp_code}")
                    self.__input_file(f"{url},{resp_code}")
                    self.mutex.release()
            except:
                pass
            self.num += 1
            print(f"\r [*]  已经搜索 {self.num} 个", end="", flush=True)

        # self.pool_lock.release()

    def __scan_catalogue(self, url):
        """扫后台"""
        if self.running:
            try:
                resp = requests.get(url, verify=False, timeout=5)
                resp_code = resp.status_code
                if resp_code in (200, 301, 302, 403):
                    self.mutex.acquire()
                    print("")
                    print(f" [+]  {url} >>> {resp_code}")
                    self.__input_file(f"{url},{resp_code}")
                    self.mutex.release()
            except:
                pass
            self.num += 1
            print(f"\r [*]  已经搜索 {self.num} 个", end="", flush=True)

    def stop(self):
        """结束程序"""
        print("")
        print(" [*]  收到,程序将在5s内结束")
        self.running = False
        self.pool.shutdown(wait=False)

    def start(self, url, mode, file_path_l="./dict/layer.txt", file_path_admin="./dict/admin_backstage"):   # 因为被导入了，这个的路径是根据main的路径

        if mode == "1":     # 子域名扫描
            url_list = url.split("//")  # 分割, 为了拼接子域名
            with open(file_path_l, "r", encoding="utf8") as f:
                names = f.readlines()

            for name in names:
                # try:
                name = name.strip()
                url_end = url_list[0] + "//" + name + "." + url_list[1]     # 拼接链接
                self.pool.submit(self.__scan_sub, url_end)
                # print(url_end)
                # threading.Thread(target=self.__scan_sub, args=(url_end, )).start()
                # except:
                #     pass
        if mode == "2":     # 后台扫描
            with open(file_path_admin, "r", encoding="utf8") as f:
                routes = f.readlines()
            for route in routes:
                route = route.strip()
                url_end = url + route   # 拼接URL
                self.pool.submit(self.__scan_catalogue, url_end)


if __name__ == '__main__':
    # while True:
    user = input(" >>> ")
    if user == "1":
        a = ScanSubdomain(5)
        keyboard.add_hotkey("q", a.stop)
        a.start("https://baidu.com/", "2")
    elif user == "2":
        pass
