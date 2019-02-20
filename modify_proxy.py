#!/usr/bin/Python
# -*- coding: utf-8 -*-
import sys



## 调用方式：python modify_proxy.py H71T3JBR2Z762HSD 07ACAA39EDD55595
if __name__ == '__main__':
    data = ''

    with open('weibo_scrapy/settings.py', 'r+', encoding='utf-8') as f:
        for line in f.readlines():
            if (line.find('proxyUser') != -1):
                line = '    "proxyUser": "%s",' % (sys.argv[1],) + '\n'
            if (line.find('proxyPass') != -1):
                line = '    "proxyPass": "%s",' % (sys.argv[2],) + '\n'
            data += line

    with open('weibo_scrapy/settings.py', 'r+', encoding='utf-8') as f:
        f.writelines(data)
