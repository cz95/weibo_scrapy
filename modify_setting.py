#!/usr/bin/Python
# -*- coding: utf-8 -*-
import sys

setting_dir = 'weibo_scrapy/settings.py'

def modify_pic_dir(pic_dir):
    data = ''
    with open(setting_dir, 'r+', encoding='utf-8') as f:
        for line in f.readlines():
            if (line.find('IMAGES_STORE') != -1):
                line = 'IMAGES_STORE = r"%s"' % (pic_dir,) + '\n'
            data += line
    return data


def modify_proxy(user, password):
    data = ''
    with open(setting_dir, 'r+', encoding='utf-8') as f:
        for line in f.readlines():
            if (line.find('proxyUser') != -1):
                line = '    "proxyUser": "%s",' % (user,) + '\n'
            if (line.find('proxyPass') != -1):
                line = '    "proxyPass": "%s",' % (password,) + '\n'
            data += line
    return data



## 调用方式：python modify_setting.py proxy H71T3JBR2Z762HSD 07ACAA39EDD55595
## 调用方式：python modify_setting.py pic_dir /Users/chenze/Desktop/cz95
if __name__ == '__main__':
    data = ""
    if sys.argv[1] == "proxy":
        data = modify_proxy(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "pic_dir":
        data = modify_pic_dir(sys.argv[2])
    with open(setting_dir, 'w', encoding='utf-8') as f:
        f.writelines(data)

