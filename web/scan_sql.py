import time

import requests
import json
import subprocess
import socket


class SqlmapCheck:

    taskid = ""
    header = {"Content-Type": "application/json"}
    data = {}

    def __init__(self):
        # 用于检测服务是否启动，通过端口检测
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        resp = sock.connect_ex(('localhost', 8775))
        if not resp == 0:
            subprocess.Popen("start_sqlmapapi.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)


    def start(self, url, proxy_mode=False, data=""):
        self.data['url'] = url

        if proxy_mode:
            # 检测请求类型  HTTPS 或 HTTP
            https_mode = url.split("://", 1)[0]
            if https_mode == "https":
                resp_proxy = requests.get("http://127.0.0.1:5010/get/?type=https")
            else:
                resp_proxy = requests.get("http://127.0.0.1:5010/get/")

            # 获取代理IP，并写入
            proxy_ip = resp_proxy.json()['proxy']
            self.data['proxy'] = f"{https_mode}://{proxy_ip}"

        if data:
            self.data['data'] = data

        # 进入下一步
        self.create_taskid()

    def create_taskid(self):

        # 获取sqlmap的taskid
        url = "http://127.0.0.1:8775/task/new"
        resp = requests.get(url)
        if "success" in resp.text:
            self.taskid = resp.json()['taskid']
            self.create_task()

    def create_task(self):

        # 创建扫描任务
        url = f"http://127.0.0.1:8775/option/{self.taskid}/set"
        resp = requests.post(url, data=json.dumps(self.data), headers=self.header)
        if "success" in resp.text:

            # todo 测试,记得删除
            print("任务设置成功")
            self.start_task()
        else:

            # todo 测试
            print("任务设置失败")

    def start_task(self):

        # 启动扫描任务
        url = f"http://127.0.0.1:8775/scan/{self.taskid}/start"
        resp = requests.post(url, data=json.dumps(self.data), headers=self.header)
        if "success" in resp.text:

            # todo 测试，记得删除
            print("任务启动成功")

            start_time = int(time.time())
            while True:
                status_url = f"http://127.0.0.1:8775/scan/{self.taskid}/status"
                status_resp = requests.get(status_url)
                if 'running' in status_resp.text:
                    print(f"\rrunning... 已运行{int(time.time())-start_time}s", end="", flush=True)
                else:
                    print(1)
                    end_url = f"http://127.0.0.1:8775/scan/{self.taskid}/data"
                    # del_url = f"http://127.0.0.1:8775/task/{self.taskid}/delete"

                    # requests.get(del_url)   # 删除SQLMAP的任务ID
                    end_resp = requests.get(end_url)

                    # print(end_resp.text)
                    self.__data_process(end_resp)
                    break
                time.sleep(1)
        else:

            # todo 测试
            print("任务启动失败")

    def __data_process(self, data):

        # 为了防止没检测到字符串而报错
        try:
            data_dirt = data.json()
            if data_dirt['data']:
                print("\n存在SQL注入")
                for i in data_dirt['data'][1]['value'][0]['data']:
                    print(data_dirt['data'][1]['value'][0]['data'][i]['title'])
                    print(data_dirt['data'][1]['value'][0]['data'][i]['payload'])
                    print("")
            else:
                print("无SQL注入")
        except:
            pass
        # print(data.json())


if __name__ == '__main__':
    map = SqlmapCheck()

    map.start("http://10.10.10.141/bang/sqli-labs-master/Less-1/?id=1")
    # map.start("http://10.10.10.141/bang/sqli-labs-master/Less-17/", proxy_mode=False, data="uname=123&passwd=123&submit=Submit")
    # map.start("http://10.10.10.141/bang/sqli-labs-master/Less-1/?id=1", proxy_mode=False)
