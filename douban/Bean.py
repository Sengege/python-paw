# -*- coding: utf-8 -*-
class URLextracter(object):
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
class DMovieEtl(URLextracter):
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
