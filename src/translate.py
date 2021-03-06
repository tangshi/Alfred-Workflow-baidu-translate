#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zjhch123
# @Date:   2018-02-12 21:08:34
# @Last Modified by:   hzzhangjiahao1@corp.netease.com
# @Last Modified time: 2018-02-12 21:14:48

import urllib2
import json
import sys
from xml.etree import ElementTree as ET
from urllib import urlencode

# Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
reload(sys)
sys.setdefaultencoding('utf-8')

# 百度翻译，支持中文⇌英文
def trans(word):
    word = word.lower()
    request = urllib2.Request('http://fanyi.baidu.com/sug?' + urlencode({'kw': word}))
    request.add_header("Host", "fanyi.baidu.com")
    result = json.load(urllib2.urlopen(request))

    translated = result.get('data')
    items = []
    for item in translated:
        items.append({
            'title': unicode(item.get('k').strip(',')),
            'subtitle': unicode(item.get('v').strip(',')),
            'arg': 'https://www.baidu.com/#ie=UTF-8&wd=%s' % (unicode(item.get('k'))),
            'icon': 'icon.jpg'
        })

    return generate_xml(items)

def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key in ('arg',):
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    return ET.tostring(xml_items)


# print(unicode(trans('china')))
# print(unicode(trans('你好')))