# -*- coding: utf-8 -*-  
import urllib
import os 
import sys
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html   

def mkdir(path):  
    #绝对路径
    path = os.path.join(os.getcwd(), path)
    #相对路径
    #path = path.strip()
    #判断参数
    if len(sys.argv) < 2:
        pass
    else:
        path = sys.argv[1] 
    #建立文件夹
    if not os.path.exists(path):
    	os.makedirs(path)
    	os.chdir(path)  
    else:   
        print '%s 文件已建立 ' % path  
         
if __name__ == '__main__':
    path = 'folder'
    mkdir(path)
    url = "http://mzzz.site/"
    print getHtml(url)