# -*- coding = utf-8 -*-
# @TIME :  12:16
# @Author : 晓晓鲸鱼
# @File : main.py
# @Software : PyCharm
# @脚本说明 :
import os
os.system("cls")
# txt = """
#
#
#
#                                      .l@@@@@@@@@@@@@@\`
#                                    /@@@@@@@@@@@O[[@@@@@@z.
#                                  /@@@@O[             [@@@@@b
#                                d@@@@[                  @@@@@@^
#                              /@@@@`                     @@@@@@.
#                             @@@@`        /@@@@@\.       @@@@@@c
#                           .@@@/        /@@@@@@@@@        @@@@@@@.
#                          .@@@/       /@@@@@@@@@@@\       @@@@@@l
#                          c@@/       `@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                         c@@@        =@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                         @@@^       /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                        c@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.
#                        c@@@        \@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                        @@@b         @@@@@@@@@@@@@@         /@@@@@@@
#                        @@@@          \@@@@@@@@@@/         /@@@@@@@
#                        c@@@@                             /@@@@@@@@
#                         ,@@@@                        /@@@@@@@@@@@
#                          @@@@@@                     @@@@@@@@@@@
#                          .c@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                              c@@@@@@@@@@@@@@@@@@@@@@@@@@b/
#                                 zg@@@@@@@@@@@@@@@@@@cb
#
#
#                                                             - v2.0
# """

txt = r"""


                                 `l?|nUOpa*#ad0z\<.
                              !/QkM8B$$@BBB@@BBBB&ZI
                             ljm&@BB@8a0v\}][\Ya%BBB*_
                         ;vM@B88B#Y]:.       "_(/{l'
                    .\o@%88%8U>
                     lOB%888%M\'
                   ~aB8888%W1.
                   ,hB888888/.
                   )B88888BQ"
                   /B88888B(                     I"
                  +888888B/                 '>jmc:
                  .Y@8888%h+            .:]vbB#t^
                  `YBB888%WOx)?~>><-{fYpM@$*vl
                    1w&BBBB@@@B%8%%@$$$8hL|I
                     .i(zZk*#MMM#abZUj}>"
                           `,;llI:"`.


"""

print(txt)


from information_gathering.scan_port import SearchPort  # 多线程扫端口
from information_gathering.scan_ip import SearchIp        # 扫IP
from enc_and_dec import fence, hash_enc, caesar, symmetric_enc_dec  # 加密解密模块
from flooding import arp, syn   # 泛洪攻击模块
from blast import scan_subdomain
import ipaddress    # 将IP段转化为多个IP
import multiprocessing
import time
from colorama import init, Fore, Style
import keyboard

# V2.0 新增
import web.scan_web_fingerprint as finger     # 指纹识别
import web.scan_web_link as link      # 爬取目录, 改代码引用了代码模块
from web import scan_web_subdomain      # 子域名扫描
from blast import mysql_blast       # Mysql爆破
from blast import redis_blast       # Redis爆破
from web import scan_web_xss        # XSS扫描
import proxy_pool       # 代理池
import subprocess       # 子进程
import web.scan_sql     # SQL扫描
import socket


class Run:

    def search_port(self):
        """
        return: 1. 搜索端口的对象 2.ip地址对象 3.用户选择进程数量
        """
        print("")
        print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
        print(
            f"{Fore.RED}║                       {Style.BRIGHT+Fore.MAGENTA}端 口 扫 描{Style.RESET_ALL}                        {Fore.RED}║")
        print(f"{Fore.RED}╚──────────────────────────────────────────────────────────╝")
        print("")

        try:
            print(f"{Style.BRIGHT+Fore.WHITE}[{Fore.BLUE}IP范围{Style.BRIGHT+Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_ip = input()

            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.YELLOW}1.{Fore.BLUE}自定端口{Style.BRIGHT + Fore.WHITE}{Fore.WHITE} "
                  f"{Fore.YELLOW}2.{Fore.BLUE}常见端口{Style.BRIGHT + Fore.WHITE}]"
                  f"{Fore.RESET} >>> ", end="")
            user_mode = input()

            if user_mode == "1":
                print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}最小端口{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
                user_min_p = int(input())
                print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}最大端口{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
                user_max_p = int(input())

            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}进程数量{Fore.WHITE}-{Fore.RED}回车{multiprocessing.cpu_count()}个{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_process = input()

            if not user_process:    # 默认为系统最大内核数
                user_process = multiprocessing.cpu_count()
            user_process = int(user_process)

            lock = multiprocessing.Lock()  # GIL锁
            if user_mode == "1":
                # user_min_p = int(input("最小端口 >>> "))
                # user_max_p = int(input("最大端口 >>> "))
                return SearchPort(user_ip, min_p=user_min_p, max_p=user_max_p, lock=lock), \
                       ipaddress.ip_network(user_ip), \
                       user_process, \
                       user_mode
            elif user_mode == "2":
                return SearchPort(user_ip,  lock=lock), \
                       ipaddress.ip_network(user_ip), \
                       user_process, \
                       user_mode
        except:
            print("输入有误，请重新选择!")

    def fence_enc(self):
        """栅栏加密"""
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}加密内容{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_data = input()
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}每组个数{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_num = int(input())

            fence.enc(user_data, user_num)
        except:
            pass

    def fence_dec(self):
        """栅栏解密"""
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}解密内容{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_data = input()
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}每组个数 {Fore.RED}回车爆破{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_num = input()

            if user_num:
                fence.dec(user_data, int(user_num))
            else:
                fence.dec(user_data)
        except:
            pass

    def caesar_enc(self):
        """凯撒加密"""
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}加密内容{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_data = input()
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}偏移位数{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_offset = int(input())

            caes = caesar.Caesar()
            resp = caes.enc(user_data, user_offset)
            print(f"\n{resp}\n")

        except:
            pass

    def caesar_dec(self):
        """凯撒解密"""
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}解密内容{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_data = input()
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}偏移位数{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_offset = int(input())

            caes = caesar.Caesar()
            resp = caes.dec(user_data, user_offset)
            print(f"\n{resp}\n")
        except:
            pass

    def base64_enc(self):
        """base64加密"""
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}加密内容{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_data = input()

            b64 = symmetric_enc_dec.Symmetric()
            resp = b64.base64_enc(user_data)
            print(f"\n{resp}\n")
        except:
            pass

    def base64_dec(self):
        """base64解密"""
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}解密内容{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_data = input()

            b64 = symmetric_enc_dec.Symmetric()
            resp = b64.base64_dec(user_data)
            print(f"\n{resp}\n")
        except:
            pass

    def md5_enc(self):
        """md5加密"""
        print(f"{Style.BRIGHT+Fore.WHITE}[{Fore.BLUE}MD5-加密内容{Style.BRIGHT+Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_data = input()

        enc = hash_enc.Hash()
        print("\n"+enc.md5(user_data)+"\n")

    def sha_enc(self):
        """sha加密"""
        os.system("cls")
        print("\n\n\n\n")
        print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
        print(f"{Fore.RED}║                       {Fore.MAGENTA}SHA 加 密{Style.RESET_ALL}                          {Fore.RED}║")
        print(f"{Fore.RED}╟──────────────────────────────────────────────────────────╢")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}1. {Style.BRIGHT + Fore.GREEN}SHA1{Style.RESET_ALL}                            {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}2. {Style.BRIGHT + Fore.GREEN}SHA224{Style.RESET_ALL}                          {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}3. {Style.BRIGHT + Fore.GREEN}SHA256{Style.RESET_ALL}                          {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}4. {Style.BRIGHT + Fore.GREEN}SHA384{Style.RESET_ALL}                          {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}5. {Style.BRIGHT + Fore.GREEN}SHA512{Style.RESET_ALL}                          {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}6. {Style.BRIGHT + Fore.GREEN}SHA3_224{Style.RESET_ALL}                        {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}7. {Style.BRIGHT + Fore.GREEN}SHA3_256{Style.RESET_ALL}                        {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}8. {Style.BRIGHT + Fore.GREEN}SHA3_384{Style.RESET_ALL}                        {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}9. {Style.BRIGHT + Fore.GREEN}SHA3_512{Style.RESET_ALL}                        {Fore.RED}║")
        print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}0. {Style.BRIGHT + Fore.GREEN}退出{Style.RESET_ALL}                            {Fore.RED}║")
        print(f"{Fore.RED}╚══════════════════════════════════════════════════════════╝")
        print("\n\n")

        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}SHA-模式选择{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_opt = input()
        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}SHA-加密内容{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_data = input()

        if user_opt in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            enc = hash_enc.Hash()
            resp = enc.sha(user_data, user_opt)    # 加密
            print(f"\n{resp}\n")
        else:
            return

    def arp_deception(self):
        """ARP欺骗"""
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}网关IP{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_ip_way = input()
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标IP{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_ip_attack = input()

            arp_user = arp.Arp()
            arp_user.start(user_ip_way, user_ip_attack, "1")    # 模式1 ARP欺骗
        except:
            pass

    def arp_attack(self):
        """ARP攻击"""
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}网关IP{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_ip_way = input()
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标IP{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_ip_attack = input()

            arp_user = arp.Arp()
            arp_user.start(user_ip_way, user_ip_attack, "2")  # 模式2 ARP攻击
        except:
            pass

    def arp_attack_way(self):
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}网关IP{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_ip_way = input()

            arp_user = arp.Arp()
            arp_user.start(user_ip_way, "", "3")  # 模式3 ARP攻击网关，使网关ARP表装满
        except:
            pass

    def syn_attak(self, mode):
        """
            SYN攻击
            mode=1: 半连接
            mode=2: 全连接
        """
        try:
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标IP{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_attack_ip = input()
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标端口{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_attack_port = int(input())

            syn_atk = syn.SYN()
            syn_atk.start(user_attack_ip, user_attack_port, mode)
        except:
            pass

    def scan_sub(self, mode):
        """
        扫描子域名和管理员后台
        mode=1: 扫描子域名
        mode=2: 扫描后台
        """
        # try:
        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标网址{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_url = input()
        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}线程数量 {Fore.RED}默认 {multiprocessing.cpu_count()}个{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_thr = input()

        if not user_thr:    # 如果用户没有输入线程，则自动加入
            user_thr = multiprocessing.cpu_count()  # 根据当前CPU核心数创建线程
        scan_web = scan_subdomain.ScanSubdomain(user_thr)   # 创建对象
        keyboard.add_hotkey("q", scan_web.stop)
        scan_web.start(user_url, mode=mode)
        # except:
        #     pass


    def finger_recog(self):
        """指纹识别"""

        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标网址{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_url = input()
        finger.main(user_url)

    def dir_scan(self):
        """目录扫描"""
        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标网址{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_url = input()
        # 如果有任何输入，则表示开
        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}代理开关 {Fore.RED}默认关闭{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_mode = input()
        if not user_mode:
            user_mode = False
        else:
            user_mode = True

        get_link = link.GetDirLink()
        get_link.start(user_url, proxy=user_mode)

    def scan_sub_domain(self):
        """子域名扫描"""

        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标网址{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_url = input()
        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}代理开关 {Fore.RED}默认关闭{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_mode = input()

        user_mode = True if user_mode else False

        scan_web_subdomain.main(user_url, user_mode)


    def mysql_passwd_blast(self):
        """mysql弱口令检测"""

        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标IP{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_ip = input()

        mysql_blast.Mysql_burst().brute(user_ip)

    def redis_scan(self):
        """redis扫描"""

        redis_blast.main()

    def xss_check(self):
        """XSS检测"""

        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}URL{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_url = input()
        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}代理开关 {Fore.RED}默认关闭{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_proxy = input()

        if user_proxy:
            xss_scan = scan_web_xss.ScanXss(user_url, proxy_mode=True)
        else:
            xss_scan = scan_web_xss.ScanXss(user_url)


        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}请求方式{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_mode = input()

        if user_mode == "post":
            # 使用 usernmae=admin&password=123&submit=submit 这种方式提交
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}提交数据{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_data = input()
            xss_scan.xss_post(user_data)

        elif user_mode == "get":
            xss_scan.xss_get()

    def sql_check(self):
        """SQL检测"""

        sql_scan = web.scan_sql.SqlmapCheck()

        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}URL{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_url = input()


        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}请求方式{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_mode = input()

        # sql_scan = scan_web_sql.ScanSql(user_url)

        if user_mode == "post":
            # 使用 usernmae=admin&password=123&submit=submit 这种方式提交
            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}提交数据{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_data = input()

        print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}代理开关 {Fore.RED}默认关闭{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        user_porxy = input()

        if user_porxy:
            if user_mode == "post":
                sql_scan.start(user_url, proxy_mode=True, data=user_data)
            else:
                sql_scan.start(user_url, proxy_mode=True)
        else:
            if user_mode == "post":
                sql_scan.start(user_url, data=user_data)
            else:
                sql_scan.start(user_url)


    def proxy_pool_start(self):
        """开启代理池"""

        # 开启代理池
        # proxy_obj = proxy_pool.ProxyPool()
        # os.system("start_proxy_pool.bat")
        subprocess.Popen("start_proxy_pool.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)

    def xray_scan(self):
        """xray扫描"""

        # print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}目标地址{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
        # user_url = input()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        resp_http_status = sock.connect_ex(('localhost', 5000))
        if not resp_http_status == 0:
            subprocess.Popen(['python', './web/scan_vul_xray.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("[*]  已开启推送接口")
        # subprocess.Popen(['necessary_environment\\xray1.9.11\\xray.exe', 'webscan', '--basic-crawler', user_url, '--webhook-output', 'http://127.0.0.1:5000/webxray'], creationflags=subprocess.CREATE_NEW_CONSOLE)


if __name__ == '__main__':
    user = Run()
    init(autoreset=True)  # 确保控制台输出彩色
    # os.system("cls")    # 清空屏幕
    # print("\n\n\n\n")
    # print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
    # print(f"{Fore.RED}║                    {Fore.MAGENTA}中 国 菜 板 v2.0{Style.RESET_ALL}                      {Fore.RED}║")
    # print(f"{Fore.RED}╟──────────────────────────────────────────────────────────╢")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}1. {Style.BRIGHT+Fore.GREEN}扫端口{Style.RESET_ALL}                          {Fore.RED}║")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}2. {Style.BRIGHT+Fore.GREEN}扫IP{Style.RESET_ALL}                            {Fore.RED}║")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}3. {Style.BRIGHT+Fore.GREEN}扫网页{Style.RESET_ALL}                          {Fore.RED}║")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}4. {Style.BRIGHT+Fore.GREEN}加解密{Style.RESET_ALL}                          {Fore.RED}║")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}5. {Style.BRIGHT+Fore.GREEN}泛洪{Style.RESET_ALL}                            {Fore.RED}║")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}6. {Style.BRIGHT+Fore.GREEN}检测{Style.RESET_ALL}                            {Fore.RED}║")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}7. {Style.BRIGHT+Fore.GREEN}代理{Style.RESET_ALL}                            {Fore.RED}║")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}9. {Style.BRIGHT+Fore.GREEN}帮助{Style.RESET_ALL}                            {Fore.RED}║")
    # print(f"{Fore.RED}║                       {Style.BRIGHT+Fore.YELLOW}0. {Style.BRIGHT+Fore.GREEN}退出{Style.RESET_ALL}                            {Fore.RED}║")
    # print(f"{Fore.RED}╚══════════════════════════════════════════════════════════╝")
    # print("\n\n")
    while True:

        print(f"{Style.BRIGHT+Fore.WHITE}[{Fore.MAGENTA}中国菜板{Style.BRIGHT+Fore.WHITE}]{Fore.RESET}", end="")
        user_option = input(" >>> ")

        if user_option == "0":    # 退出
            break
        elif user_option == "9":
            print("\n\n\n\n")
            print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                    {Fore.MAGENTA}中 国 菜 板 v2.0{Style.RESET_ALL}                      {Fore.RED}║")
            print(f"{Fore.RED}╟──────────────────────────────────────────────────────────╢")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}1. {Style.BRIGHT + Fore.GREEN}扫端口{Style.RESET_ALL}                          {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}2. {Style.BRIGHT + Fore.GREEN}扫IP{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}3. {Style.BRIGHT + Fore.GREEN}扫网页{Style.RESET_ALL}                          {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}4. {Style.BRIGHT + Fore.GREEN}加解密{Style.RESET_ALL}                          {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}5. {Style.BRIGHT + Fore.GREEN}泛洪{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}6. {Style.BRIGHT + Fore.GREEN}检测{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}7. {Style.BRIGHT + Fore.GREEN}代理{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}0. {Style.BRIGHT + Fore.GREEN}退出{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════╝")
            print("\n\n")

        elif user_option == "1":  # 端口扫描
            # port_object:扫端口的对象, ip_object:ip段对象, pool_num: 进程数量, mode: 用户选择的模式
            port_object, ip_object, pool_num, mode = user.search_port()

            pool = multiprocessing.Pool(pool_num)   # 进程池数量
            start = time.time()
            # 遍历出所有IP
            for addr in ip_object.hosts():
                pool.apply_async(func=port_object.start, args=(str(addr), mode))

            pool.close()
            pool.join()

            end = time.time()
            print(" [*]  扫描完毕，用时: " + str(int(end - start)) + " s")

        elif user_option == "2":    # IP扫描
            print("\n\n\n")
            print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
            print(
                f"{Fore.RED}║                       {Style.BRIGHT + Fore.MAGENTA}I P 扫 描{Style.RESET_ALL}                          {Fore.RED}║")
            print(f"{Fore.RED}╚──────────────────────────────────────────────────────────╝")
            print("\n")
            try:
                print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}IP范围{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
                user_input_ip_range = input()

                scanip = SearchIp()
                scanip.start(user_input_ip_range)
            except:
                print(f"\n{Style.BRIGHT + Fore.WHITE}[{Fore.RED} 输入有误！{Style.BRIGHT + Fore.WHITE}]{Fore.RESET}\n")

        elif user_option == "3":
            os.system("cls")
            print("\n\n\n\n")
            print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                      {Fore.MAGENTA}网 页 扫 描{Style.RESET_ALL}                         {Fore.RED}║")
            print(f"{Fore.RED}╟──────────────────────────────────────────────────────────╢")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}1. {Style.BRIGHT + Fore.GREEN}子域名{Style.RESET_ALL}                          {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}2. {Style.BRIGHT + Fore.GREEN}目录{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}3. {Style.BRIGHT + Fore.GREEN}指纹{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════╝")
            print("\n\n")

            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}网页扫描{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_scan_opt = input()


            if user_scan_opt == "1":        # 子域名扫描
                user.scan_sub_domain()
            elif user_scan_opt == "2":      # 目录扫描
                user.dir_scan()
            elif user_scan_opt == "3":      # 指纹识别
                user.finger_recog()


        elif user_option == "4":    # 加解密
            os.system("cls")
            print("\n\n\n\n")
            print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                      {Fore.MAGENTA}加 密 解 密{Style.RESET_ALL}                         {Fore.RED}║")
            print(f"{Fore.RED}╟──────────────────────────────────────────────────────────╢")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}1. {Style.BRIGHT + Fore.GREEN}栅栏加密{Style.RESET_ALL}                        {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}2. {Style.BRIGHT + Fore.GREEN}栅栏解密{Style.RESET_ALL}                        {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}3. {Style.BRIGHT + Fore.GREEN}凯撒加密{Style.RESET_ALL}                        {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}4. {Style.BRIGHT + Fore.GREEN}凯撒解密{Style.RESET_ALL}                        {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}5. {Style.BRIGHT + Fore.GREEN}base64加密{Style.RESET_ALL}                      {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}6. {Style.BRIGHT + Fore.GREEN}base64解密{Style.RESET_ALL}                      {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}7. {Style.BRIGHT + Fore.GREEN}md5加密{Style.RESET_ALL}                         {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}8. {Style.BRIGHT + Fore.GREEN}sha加密{Style.RESET_ALL}                         {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}0. {Style.BRIGHT + Fore.GREEN}退出{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════╝")
            print("\n\n")

            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}加密解密{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_enc_dec = input()

            if user_enc_dec == "1":     # 栅栏加密
                user.fence_enc()
            elif user_enc_dec == "2":   # 栅栏解密
                user.fence_dec()
            elif user_enc_dec == "3":   # 凯撒加密
                user.caesar_enc()
            elif user_enc_dec == "4":   # 凯撒解密
                user.caesar_dec()
            elif user_enc_dec == "5":   # base64加密
                user.base64_enc()
            elif user_enc_dec == "6":   # base64解密
                user.base64_dec()
            elif user_enc_dec == "7":    # md5加密
                user.md5_enc()
            elif user_enc_dec == "8":   # sha加密
                user.sha_enc()

        elif user_option == "5":
            os.system("cls")
            print("\n\n\n\n")
            print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
            print(f"{Fore.RED}║                      {Fore.MAGENTA}泛 洪 攻 击{Style.RESET_ALL}                         {Fore.RED}║")
            print(f"{Fore.RED}╟──────────────────────────────────────────────────────────╢")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}1. {Style.BRIGHT + Fore.GREEN}ARP欺骗{Style.RESET_ALL}                         {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}2. {Style.BRIGHT + Fore.GREEN}ARP攻击{Style.RESET_ALL}                         {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}3. {Style.BRIGHT + Fore.GREEN}ARP攻击网关{Style.RESET_ALL}                     {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}4. {Style.BRIGHT + Fore.GREEN}SYN半连接{Style.RESET_ALL}                       {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}5. {Style.BRIGHT + Fore.GREEN}SYN全连接{Style.RESET_ALL}                       {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}0. {Style.BRIGHT + Fore.GREEN}退出{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════╝")
            print("\n\n")

            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}泛洪攻击{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_flood_opt = input()
            if user_flood_opt == "1":       # ARP欺骗
                user.arp_deception()
            elif user_flood_opt == "2":     # ARP攻击
                user.arp_attack()
            elif user_flood_opt == "3":     # ARP攻击路由器ARP表
                user.arp_attack_way()
            elif user_flood_opt == "4":     # SYN半连接攻击
                user.syn_attak("1")
            elif user_flood_opt == "5":     # SYN全连接攻击
                user.syn_attak("2")

        elif user_option == "6":
            os.system("cls")
            print("\n\n\n\n")
            print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
            print(
                f"{Fore.RED}║                      {Fore.MAGENTA}漏 洞 扫 描{Style.RESET_ALL}                         {Fore.RED}║")
            print(f"{Fore.RED}╟──────────────────────────────────────────────────────────╢")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}1. {Style.BRIGHT + Fore.GREEN}MySQL爆破{Style.RESET_ALL}                       {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}2. {Style.BRIGHT + Fore.GREEN}Redis爆破{Style.RESET_ALL}                       {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}3. {Style.BRIGHT + Fore.GREEN}SQL注入检测{Style.RESET_ALL}                     {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}4. {Style.BRIGHT + Fore.GREEN}XSS注入检测{Style.RESET_ALL}                     {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}5. {Style.BRIGHT + Fore.GREEN}Xray检测推送{Style.RESET_ALL}                    {Fore.RED}║")
            print(f"{Fore.RED}║                       {Style.BRIGHT + Fore.YELLOW}0. {Style.BRIGHT + Fore.GREEN}退出{Style.RESET_ALL}                            {Fore.RED}║")
            print(f"{Fore.RED}╚══════════════════════════════════════════════════════════╝")
            print("\n\n")

            print(f"{Style.BRIGHT + Fore.WHITE}[{Fore.BLUE}漏洞扫描{Style.BRIGHT + Fore.WHITE}]{Fore.RESET} >>> ", end="")
            user_scan_opt = input()

            if user_scan_opt == "1":       # Mysql弱密码爆破
                user.mysql_passwd_blast()
            elif user_scan_opt == "2":       # Redis扫描
                user.redis_scan()
            elif user_scan_opt == "3":       # SQL注入检测
                user.sql_check()
            elif user_scan_opt == "4":       # XSS检测
                user.xss_check()
            elif user_scan_opt == "5":       # Xray漏洞检测
                user.xray_scan()

        elif user_option == "7":
            user.proxy_pool_start()

