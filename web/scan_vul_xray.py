# -*- coding = utf-8 -*-
# @TIME :  19:00
# @Author : 晓晓鲸鱼
# @File : scan_vul_xray.py
# @Software : PyCharm
# @脚本说明 :

from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/webxray', methods=['POST'])
def xray_work():

    # 推送的地址
    url = "https://sctapi.ftqq.com/SCT149074TqrEUVNWrD0RItbdJvrldbMzI.send?title=Xray find VULN!"
    try:
        vul = request.json
        content = f"""
        ### xray 发现了新漏洞
        url: {vul['data']['target']['url']}
        插件: {vul['data']['plugin']}
        漏洞类型: {vul['type']}
        """
        data = {
            "desp": content
        }
        requests.post(url, data=data)

    except:
        pass


if __name__ == '__main__':
    app.run()
