# -*- coding = utf-8 -*-
# @TIME :  10:38
# @Author : 晓晓鲸鱼
# @File : symmetric_enc_dec.py
# @Software : PyCharm
# @脚本说明 : 对称加密解密
import base64


class Symmetric:

    def base64_enc(self, data):
        """base64加密"""
        data = data.encode("utf8")
        data_enc = base64.b64encode(data).decode("utf8")
        return data_enc

    def base64_dec(self, data):
        """base64解密"""
        data = data.encode("utf8")
        data_dec = base64.b64decode(data).decode("utf8")
        return data_dec


if __name__ == '__main__':
    a = Symmetric()
    resp = a.base64_enc("TVRJeg==")
    print(resp)


