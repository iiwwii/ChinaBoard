#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pythonProject1 
@File    ：爬虫.py
@Author  ：林香
@Date    ：2023/7/14 14:31 
@脚本说明：
"""
import json
import requests
import csv
import configparser
import time


class FingerprintAPI:
    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies

    def extract(self, target):
        data_dict = {}
        data = {"target": target}
        response = requests.post(self.url, cookies=self.cookies, params=data)

        # 处理响应结果
        if response.status_code == 200:
            data = response.text
            try:
                # 解析返回的json数据
                parsed_data = json.loads(data)
                # 判断返回的数据，如果有列表就把列表中的数据提取出来
                if 'FrontFrame' in parsed_data:
                    frontframe_list = parsed_data['FrontFrame']
                    if len(frontframe_list) > 0:
                        # 提取列表中的元素并赋给字段
                        data_dict['前端框架'] = frontframe_list[0]

                data_dict['url'] = parsed_data['res']['url']
                data_dict['ip'] = parsed_data['res']['ip']
                data_dict['domain'] = parsed_data['res']['domain']
                data_dict['cms'] = parsed_data['res']['cms']
                data_dict['操作系统'] = parsed_data['res']['os']
                data_dict['旁站'] = parsed_data['res']['pangzhan']
                data_dict['waf'] = parsed_data['res']['waf']

                if 'title' in parsed_data['res']['finger']:
                    info = json.loads(parsed_data['res']['finger'])
                    data_dict['网站标题'] = info['title']
                    data_dict['中间件'] = info['httpserver']

                if 'banner' in parsed_data['res']:
                    banner_data = json.loads(parsed_data['res']['banner'])

                    if 'FrontFrame' in banner_data:
                        frontframe_list = banner_data['FrontFrame']
                        if len(frontframe_list) > 0:
                            data_dict['前端框架'] = frontframe_list

                    if 'FrameWork' in banner_data:
                        framework_list = banner_data['FrameWork']
                        if len(framework_list) > 0:
                            data_dict['框架'] = framework_list

                if 'isp' in parsed_data['res']['ip_gps_info']:
                    isp_info = json.loads(parsed_data['res']['ip_gps_info'])
                    data_dict['isp'] = isp_info['isp']
                    data_dict['area'] = isp_info['area']
                    data_dict['GPS'] = isp_info['gps']

            except json.JSONDecodeError:
                print("[-]  解析json数据失败")
            except KeyError as e:
                print("[-]  提取字段时发生错误：" + str(e))

        else:
            print("[-]  请求失败，状态码：" + str(response.status_code))
        return data_dict


# 定义方法：返回的数据是列表，进行处理
def remove(result):
    # 去除前端框架字段值中的方括号
    if '前端框架' in result:
        lists = result['前端框架']
        if isinstance(lists, list):
            lists_str = ",".join(lists)
            result['前端框架'] = lists_str

    # 去除框架字段值中的方括号
    if '框架' in result:
        framework_list = result['框架']
        if isinstance(framework_list, list):
            framework_str = ",".join(framework_list)
            result['框架'] = framework_str

    # 去除cms字段值中的方括号
    if 'cms' in result:
        cms_value = result['cms']
        if isinstance(cms_value, str):
            cms_value = cms_value.strip('[]"')
            result['cms'] = cms_value
    # 去除旁站字段值中的方括号
    if '旁站' in result:
        pangzhan_value = result['旁站']
        if isinstance(pangzhan_value, list):
            if len(pangzhan_value) == 0:
                result['旁站'] = ''
            else:
                # 将列表转换为字符串
                pangzhan_str = ', '.join(pangzhan_value)
                result['旁站'] = pangzhan_str
        elif isinstance(pangzhan_value, str) and pangzhan_value == '[]':
            result['旁站'] = ''

    # 去除操作系统字段值中的引号
    if '操作系统' in result:
        os_value = result['操作系统']
        if isinstance(os_value, str):
            os_value = os_value.strip('"')
            result['操作系统'] = os_value

    return result


def main(domain):

    # 读取配置文件的cookie信息
    config = configparser.ConfigParser()
    with open("./conf/conf.ini", "r", encoding="utf-8") as f:
        config.read_file(f)
    cookie = config.get('finger', 'phpsessid')

    # 创建FingerprintAPI对象
    api = FingerprintAPI("http://finger.tidesec.com/home/index/reget", {
        "think_var": "zh-cn",
        # "PHPSESSID": "1c1o4ivkpr8neakm0u06ifdav1",
        "PHPSESSID": cookie,
        "__51cke__": "",
        "__tins__19980795": "%7B%22sid%22%3A%201689385344204%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201689387230751%7D",
        "__51laig__": "3"
    })

    # 使用extract方法进行指纹接口查询
    result = api.extract("woniuxy.com")

    # 处理返回的数据
    processed_result = remove(result)

    # 指定CSV文件
    csv_filename = f'./scan/scan_finder_{domain}_{int(time.time())}.csv'

    # 写入CSV文件
    with open(csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = processed_result.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 检查文件是否为空，如果是则写入表头
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(processed_result)

    # 在命令行输出信息
    for info in processed_result:
        print(f"[+]  {info} -> {processed_result[info]}")

    print(f"[*]  数据已写入: {csv_filename}")


if __name__ == '__main__':
    main("woniuxy.com")
