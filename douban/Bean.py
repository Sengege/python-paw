# -*- coding: utf-8 -*-
import time
class UrlExtracter(object):
    """
    初始时候指定默认为本地的Redis数据库保存 URL数据
    如果需要连接远程的数据库
    需要指定
    h=  服务器地址
    p=  redis端口
    pwd= redis设置的密码 如果无验证就为空
    """
    def __init__(self,h='localhost',p='6379',pwd=''):
        self.h=h
        self.p=p
        self.pwd=pwd
        try:
            from redis import Redis
        except:
            print "Exception: Redis dev not find"
        self.redis=Redis(host=self.h,port=self.p,db=0,password=self.pwd)
        self.setTools()

    def getRedis(self):
        return self.redis
    def setTools(self):
        try:
            import requests as paw
            from bs4 import BeautifulSoup as bp
            import os
            import re
        except:
            print "Not find requests lib or bs4 lib"


        self.paw=paw
        self.bp=bp
        self.os=os
        self.re=re

    def run(self,index):
        pass
    def saveRset(self,key,value):
        self.redis.sadd(key,value)
    def saveRlist(self,key,value):
        self.redis.lpush(key,value)
    def getRset(self,key):
        v=self.redis.spop(key)
        self.out=str(key) + '-output'
        self.redis.sadd(self.out,v)
        return v
class DMovieEtl(UrlExtracter):
    step1='dbmv-step1'
    step2='dbmv-step2'
    start_page='https://movie.douban.com/tag'

    agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
    hd = {
            "Referer":	"https://movie.douban.com/",
            "User-Agent" : agent,
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

        }

    def step_one(self):


        #得到response响应的对象
        response=self.paw.get(url=self.start_page,headers=self.hd)
        #转化字符串的网页源文件到Soup的page对象
        if(response.status_code!=200):
            print 'status_code: '+ str(response.status_code) +' from get_tags_url process'
            os._exit()
        soup_page=self.bp(response.text,'lxml')
        #找到所有到标签名
        tags=soup_page.find_all('a',href=self.re.compile('^/tag'))
        tagurl_base="https://movie.douban.com/tag/"
        #通过得到到tag构造URL
        for tag in tags:
            end_url=tagurl_base+tag.text
            print end_url
            self.saveRset(self.step1,end_url)
    def step_two(self):
        tgurl=self.getRset(self.step1)
        while(tgurl is not None):
            url=tgurl
            print "Start tag:!!!!",url
            while(len(url)!=0):
                url=self.get_urls(url)
                #print(url)
            tgurl=self.getRset(self.step1)


    def get_urls(self,u):
        response=self.paw.get(u)
        #得到response响应的对象
        if(response.status_code!=200):
            print(response.status_code)
            raise Exception("Exception throws")

        soup_page=self.bp(response.text,'lxml')
        #转化字符串的网页源文件到Soup的page对象
        raw_urls=soup_page.find_all('a',href=self.re.compile('^https://movie.douban.com/subject/'))

        for temp in raw_urls:
            #print temp['href']

            self.saveRset(self.step2,temp['href'])
        try:
            raw_total=soup_page.find('span',class_='thispage')
            total=int(raw_total['data-total-page'])
            print total
            #得到下一页的地址
            #"""!!!
            nextpage=raw_total.find_next('a',href=self.re.compile('^https://movie.douban.com/tag/.*type=T$'))['href']
        except Exception,e:
            print e
            nextpage=''
        print 'NextPage!!!!!!!:',nextpage
        return nextpage
    def run(self):
        pass

class PageExtracter(object):
    """
        默认使用mongoDB来保存 通过URL解析到到页面

    """
    step2='dbmv-step2'
    from pymongo import MongoClient
    import requests as paw
    from bs4 import BeautifulSoup as bp
    import os
    import re
    def __init__(self,h='localhost',p='6379',pwd=''):
        self.host=h

        #url = 'mongodb://' + 'tristan' + ':' + 'sengehahaha' + '@' + 'zp.tristan.pub' + ':' + '10011' +'/'+ 'douban'

        self.client = self.MongoClient(self.host,10011)

        self.db = self.client.douban

        self.p=p
        self.pwd=pwd
        try:
            from redis import Redis
        except:
            print "Exception: Redis dev not find"
        self.redis=Redis(host=self.host,port=self.p,db=0,password=self.pwd)

    def getPage(self,url):
        print(url)
        response=self.paw.get(url)
        mv=dict()
        if(response.status_code!=200):
            print(response.status_code)
            print("Exit from Exception")
            exit()
        try:
            soup_page=self.bp(response.text,'lxml')
            name=soup_page.find('span',property="v:itemreviewed").text
            year=soup_page.find('span',class_="year").text
            mv_info=soup_page.find('div',class_="indent clearfix")
            mv_img=mv_info.find('img',src=self.re.compile('^https://.*.doubanio.com/'))
            rating_num=soup_page.find('div',class_='rating_self clearfix').find('strong',class_='ll rating_num')
            mv_id=self.re.search(r'[0-9].*[0-9]',url).group(0)
            mv['name']=name
            mv['year']=year
            mv['img']=mv_img['src']
            print(rating_num.text)
            mv['rating']=float(rating_num.text)  #new modify to int for pick
            #mv['info']=mv_info
            mv['id']=mv_id
        except Exception,e:
            print e
            print(url)
            print("Raise a Exception")
            mv=None

        return mv
    def getRset(self,key):
        v=self.redis.spop(key)
        self.out=str(key) + '-output'
        self.redis.sadd(self.out,v)
        return v
    def run(self):

        url=self.getRset(self.step2)
        while(url is not None):
            mv=self.getPage(url)
            if(mv is not None):
                a=self.db.mv_test1.find_one({"id":mv['id']})
                if(a is None):
                    status=self.db.mv_test1.insert_one(mv)
                    print(type(status))
                    print(status)
                    print("insert success")
                else:
                    print("Failed,id exist")

            else:
                print(url)
                print '解析失败'
            time.sleep(30)
            url=self.getRset(self.step2)
