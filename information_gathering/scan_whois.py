# -*- coding = utf-8 -*-
# @TIME :  22:57
# @Author : 晓晓鲸鱼
# @File : scan_whois.py
# @Software : PyCharm
# @脚本说明 :

from whois import whois


class Whois:

    def search_whois(self, url):
        resp = whois(url)
        return whois()


if __name__ == '__main__':
    a = Whois()
    a.search_whois("821821.top")

