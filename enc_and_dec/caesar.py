# -*- coding = utf-8 -*-
# @TIME :  10:11
# @Author : 晓晓鲸鱼
# @File : caesar.py
# @Software : PyCharm
# @脚本说明 :


class Caesar:

    def enc(self, data, offset_num):
        data_enc = ""
        for word in data:
            w = ord(word)+offset_num
            data_enc += chr(w)
        return data_enc

    def dec(self, data, offset_num):
        data_dec = ""
        for word in data:
            w = ord(word)-offset_num
            data_dec += chr(w)
        return data_dec


if __name__ == '__main__':
    a = Caesar()
    resp = a.dec("卭樃", 6)
    print(resp)