#-*-coding=utf-8-*-
from bs4 import BeautifulSoup
import urllib2
import sys
import StringIO
import gzip
import time
import random
import re
import urllib
import os
reload(sys)
sys.setdefaultencoding('utf-8')

class Xitek():
    def __init__(self):
        self.url="http://photo.xitek.com/"
        user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.headers={"User-Agent":user_agent}
        self.last_page=self.__get_last_page()


    def __get_last_page(self):
        html=self.__getContentAuto(self.url)
        bs=BeautifulSoup(html,"html.parser")
        page=bs.find_all('a',class_="blast")
        last_page=page[0]['href'].split('/')[-1]
        return int(last_page)


    def __getContentAuto(self,url):
        req=urllib2.Request(url,headers=self.headers)
        resp=urllib2.urlopen(req)
        #time.sleep(2*random.random())
        content=resp.read()
        info=resp.info().get("Content-Encoding")
        if info==None:
            return content
        else:
            t=StringIO.StringIO(content)
            gziper=gzip.GzipFile(fileobj=t)
            html = gziper.read()
            return html

    def __download(self,url):
        p=re.compile(r'href="(/photoid/\d+)"')

        html=self.__getContentAuto(url)

        content = p.findall(html)
        for i in content:
            print(i)
            photoid=self.__getContentAuto(self.url+i)
            bs=BeautifulSoup(photoid,"html.parser")
            final_link=bs.find('img',class_="mimg")['src']
            #print final_link
            title=bs.title.string.strip()
            filename = re.sub('[\/:*?"<>|]', '-', title)
            filename=filename+'.jpg'
            try:
                print(filename)
                print(final_link)
                urllib.urlretrieve(final_link,filename)
                time.sleep(5)
            except :
                pass
                print("download file fail")

    def getPhoto(self):
        start=0
        #use style/0
        photo_url="http://photo.xitek.com/style/0/p/"
        for i in range(start,self.last_page+1):
            url=photo_url+str(i)
            print(url)
            time.sleep(1)
            self.__download(url)

def mkdir(path):
    sub_folder = os.path.join(os.getcwd(), path)
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    os.chdir(sub_folder)

if __name__=="__main__":
    path = 'content'
    mkdir(path)
    obj=Xitek()
    obj.getPhoto()
