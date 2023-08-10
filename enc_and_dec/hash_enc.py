# -*- coding = utf-8 -*-
# @TIME :  10:53
# @Author : 晓晓鲸鱼
# @File : hash_enc.py
# @Software : PyCharm
# @脚本说明 :

import hashlib

class Hash:
    def sha(self, data, mode):
        if mode == "1":
            sha = hashlib.sha1()                # 创建sha对象   (对象）
        elif mode == "2":
            sha = hashlib.sha224()
        elif mode == "3":
            sha = hashlib.sha256()
        elif mode == "4":
            sha = hashlib.sha384()
        elif mode == "5":
            sha = hashlib.sha512()
        elif mode == "6":
            sha = hashlib.sha3_224()
        elif mode == "7":
            sha = hashlib.sha3_256()
        elif mode == "8":
            sha = hashlib.sha3_384()
        elif mode == "9":
            sha = hashlib.sha3_512()
        sha.update(data.encode("utf8"))     # 转换为utf字节流 (对象)
        sha = sha.hexdigest()               # 转换为16进制字符串 (字符串)
        return sha

    def md5(self, data):
        md5 = hashlib.md5()
        md5.update(data.encode("utf8"))
        md5 = md5.hexdigest()
        return md5


if __name__ == '__main__':
    a = Hash()
    # resp = a.sha("123", "5")
    # print(resp)
    resp = a.md5("12uyikgui3")
    print(resp)