# -*- coding = utf-8 -*-
# @TIME :  19:55
# @Author : 晓晓鲸鱼
# @File : fence.py
# @Software : PyCharm
# @脚本说明 :

# -*- coding = utf-8 -*-
# @TIME :  20:15
# @Author : 晓晓鲸鱼
# @File : 栅栏加密解密.py
# @Software : PyCharm
# @脚本说明 :


def dec(data, user_num=0):
    """
    栅栏解密脚本
    输入加密值可返回多种排列可能
    """

    # 知道加密组数，进行每组加密
    if user_num:
        l = []
        l_1 = []
        min, max = 0, 0
        length = int(len(data) / user_num)
        length_remainder = int(len(data) % user_num)
        for j in range(user_num):
            # 如果有余数，则进入
            if length_remainder:
                length_remainder -= 1  # 余数-1
                max += length + 1  # 有余数，则输出的时候多加个字符
                l_1.append(data[min:max])
                min += length + 1
            # 如果没有余数，则进入
            else:
                max += length
                l_1.append(data[min:max])
                min += length

        # 将每行数据加入到大列表中
        l.append(l_1)

    # 不知道加密组数，列出所有可能性
    else:
        line_num = int(len(data) - 1)

        l = []
        for line in range(2, line_num+1):    # 从2到最大行数遍历
            l_1 = []

            min, max = 0, 0     # 截取字符串的开始和结尾
            length = int(len(data) / line)      # 计算每行最大的字符个数
            length_remainder = int(len(data) % line)    # 计算余数个数

            # 将数据分成多行
            for j in range(line):
                # 如果有余数，则进入
                if length_remainder:
                    length_remainder -= 1   # 余数-1
                    max += length+1     # 有余数，则输出的时候多加个字符
                    l_1.append(data[min:max])
                    min += length+1
                # 如果没有余数，则进入
                else:
                    max += length
                    l_1.append(data[min:max])
                    min += length

            # 将每行数据加入到大列表中
            l.append(l_1)


    # 将列表的值拼接好，并成行返回
    for ll in l:     # 拿取每个列表
        str_data = ""   # 空字符串，存放每行的值
        for word_num in range(len(ll[0])):  # 拿取第一个元素的字符数，后面会以这个数量为基准
            for num in range(len(ll)):    # 拿取列表元素的个数
                if word_num > len(ll[num]) - 1:   # 如果元素的索引大于了固有索引值，则退出循环
                    break
                str_data += ll[num][word_num]
        print(str_data, end="\n\n")


def enc(data, type_num):
    # if type(type_num) != int:
    #     print("请输入整数偏移量")
    #     return

    l = []
    # 先创建行数相对的元素
    for i in range(type_num):
        l.append("")

    # 将每组数据写入列表中
    for i in range(len(data)):
        for j in range(type_num):
            # 判断是哪组的数据
            if i % type_num == j:  # 精髓
                l[j] += data[i]
    # 将列表的数据转为字符串并输出
    str_ = ""
    for i in l:
        str_ += i
    print(f"\n{str_}\n")


if __name__ == '__main__':
    # # 原文: 一二三四五六七八九十壹
    # no("一五九二六十三七壹四八")

    # no("一七二八三四五六")
    # while True:
    #     user_option = input("1加密,2解密,0退出 >>> ")
    #     if user_option == "1":
    #         try:
    #             user_data = input("加密内容 >>> ")
    #             user_num = int(input("每组字数 >>> "))
    #             enc(user_data, user_num)
    #         except TypeError:
    #             pass
    #     elif user_option == "2":
    #         user_data_1 = input("解密内容 >>> ")
    #         dec(user_data_1)
    #     elif user_option == "0":
    #         break
    #     else:
    #         pass

    dec("172839456", 6)

