#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
import re
import os
import sys
import urllib
import urllib2
from PIL import Image



#根据给定的网址来获取网页详细信息
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

#创建保存图片的文件夹
def mkdir(path):
    path = path.strip()
    # 判断路径是否存在
    isExists = os.path.exists(path)
    if not isExists:
        print u'新建',path,u'的文件夹'
        os.makedirs(path)
        return True
    else:
        #print u'名为',path,u'的文件夹已创建'
        return False

#获取网页中所有图片的地址
def getAllImg(html):
    #利用正则表达式把源代码中的图片地址过滤出来
    reg = r'src="(.*?\.(?:png|jpg|jpeg))" width'
    #[(jpg)(jpeg)(png)(bmp)]
    imgre = re.compile(reg)
    #表示在整个网页中过滤出所有图片的地址，放在imglist中
    imglist = imgre.findall(html)
    return imglist

# 保存多张图片
def saveImages(imglist,name):
    number = 1
    for imageURL in imglist:
        splitPath = imageURL.split('.')
        fTail = splitPath.pop()
        if len(fTail) > 3:
            fTail = 'jpg'
        fileName = name + "/" + str(number) + "." + fTail
        # 对于每张图片地址，进行保存
        try:
            u = urllib2.urlopen(imageURL)
            data = u.read()
            f = open(fileName,'wb+')
            f.write(data)
            print '正在保存的一张图片为',fileName
            f.close()
        except urllib2.URLError as e:
            print (e.reason)
        number += 1

#转换图片格式像化
def preprocessed_image(image):
    img = image_ifo(image)
    if not img.mode == 'YCbCr':
        img = img.convert('YCbCr')
    return img
def image_ifo(image):
    try:
        img = Image.open(image)
    except Exception,e:
        print "Can not open the image!"
    #显示图片像素大小
    #print 'Image Mode:%s,Image Size:%s,Image Format:%s' % (img.mode,img.size,img.format)
    return img

#检测像素肤色比例（YCBCR模型）
def detector(image):
    img = preprocessed_image(image)
    ycbcr_data = img.getdata()
    W,H = img.size
    #设定像素比例值
    THRESHOLD = 0.5
    count = 0
    for i,ycbcr in enumerate(ycbcr_data):
        y,cb,cr = ycbcr
        #if 80 <= cb <= 120 and 133 <= cr <= 173:
        if 86 <= cb <= 127 and 130 <= cr < 168:
            #计算像素为肤色的个数
            count += 1
    if count > THRESHOLD*W*H:
        #print 'The image is pornographic!'
        return True
    else:
        #print 'The image is not pornographic!'
        return False

#创建本地保存文件夹，并下载保存图片进行判定
if __name__ == '__main__':
    html = getHtml("http://www.umei.cc/meinvtupian/meinvmote/")
    path = 'pic'
    mkdir(path)
    imglist = getAllImg(html)
    #print imglist
    saveImages(imglist,path)
    picdir = os.listdir(path)
    os.chdir(path)
    os.getcwd()
    for image in picdir:
        if detector(image):
            #print u'检测到了美女图片'
            pass
        else:
            os.remove(image)
