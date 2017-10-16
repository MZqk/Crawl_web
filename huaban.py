#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import re
import urllib2
import os
import urllib
import time
import random
from PIL import Image  

beauty_url = "http://huaban.com/favorite/beauty/"
pin_re = '<a href="/pins/(.+?)/"'

def mkdir(path):
    if len(sys.argv) < 2:
        local_path = path
    else:
        local_path = sys.argv[1]
    if not os.path.exists(local_path):
        try:
            os.makedirs(local_path)
        except e:
            print e
            sys.exit(1)
    print "pin images will saved to: %s" % local_path

def getpage():
    #将网页缓存至临时目录（windows不支持curl）
    os.system("curl -s %s -o /tmp/huaban.html" % beauty_url)
    #读取整个网页
    content = open("/tmp/huaban.html").read()
    pins = re.findall(pin_re, content)[1:]
    return pins

def get_img_url(pin):
    #获取新的url
    pin_url = "http://huaban.com/pins/%s/" % pin
    img_url_re = '<img alt=".+?" src="(.+?)"'
    #从新的url中读取网页内容
    pg = urllib2.urlopen(pin_url)
    content = pg.read()
    pg.close()
    time.sleep(2*random.random())
    try:
        img_url = re.findall(img_url_re, content)[0]
        time.sleep(2*random.random())
    except:
        print re.findall(img_url_re, content)
        sys.exit(1)
    return img_url
    
if __name__ == "__main__":
    path = "./huaban"
    mkdir(path)
    pins = getpage()
    
    for pin in pins:
        img_url = get_img_url(pin)
        img_date = "http:" + img_url
        urllib.urlretrieve(img_date, "%s/%s.jpeg" % (path,pin))
        picdir = '%s/%s.jpeg' %  (path,pin)
        print '正在保存图片 %s' % picdir

