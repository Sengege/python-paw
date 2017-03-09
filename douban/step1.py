# -*- coding: utf-8 -*-
import requests as paw
from bs4 import BeautifulSoup
import Queue
import re
import os
from redis import Redis
r=Redis()
#requests 用来处理http请求
#bs4用来进行页面的解析
# 构造 Request headers
def get_tags_url():

    agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
    hd = {
        "Referer":	"https://movie.douban.com/",
        "User-Agent" : agent,
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

    }
    url_q = Queue.Queue()
    tags_set=set()
    u="https://movie.douban.com/tag" #豆瓣标签地址
    # 使用登录cookie信息
    response=paw.get(url=u,headers=hd)#得到response响应的对象
    #response=paw.get('https://www.baidu.com')
    soup_page=BeautifulSoup(response.text,'lxml')#转化字符串的网页源文件到Soup的page对象
    if(response.status_code!=200):
        print 'status_code: '+ str(response.status_code) +' from get_tags_url process'
        os._exit()

#    raw_input()  测试断点
    tags=soup_page.find_all('a',href=re.compile('^/tag'))#找到所有到标签名

    tagurl_base="https://movie.douban.com/tag/" #通过得到到tag构造URL

    for tag in tags:
        end_url=tagurl_base+tag.text
        tags_set.add(end_url)
        #print(end_url)
        url_q.put(end_url)

    print 'total tags :'+str(len(tags_set))
    #raw_input() #断点 在得到所有tags URL处
    return url_q

def get_tags_url_toRedis():

    agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
    hd = {
        "Referer":	"https://movie.douban.com/",
        "User-Agent" : agent,
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

    }
    url_q = Queue.Queue()
    tags_set=set()
    u="https://movie.douban.com/tag" #豆瓣标签地址
    # 使用登录cookie信息
    response=paw.get(url=u,headers=hd)#得到response响应的对象
    #response=paw.get('https://www.baidu.com')
    soup_page=BeautifulSoup(response.text,'lxml')#转化字符串的网页源文件到Soup的page对象
    if(response.status_code!=200):
        print 'status_code: '+ str(response.status_code) +' from get_tags_url process'
        os._exit()

#    raw_input()  测试断点
    tags=soup_page.find_all('a',href=re.compile('^/tag'))#找到所有到标签名

    tagurl_base="https://movie.douban.com/tag/" #通过得到到tag构造URL

    for tag in tags:
        end_url=tagurl_base+tag.text
        tags_set.add(end_url)
        #print(end_url)
        url_q.put(end_url)
        r.lpush("tag_urls",end_url)
    print 'total tags :'+str(len(tags_set))
    #raw_input() #断点 在得到所有tags URL处
    return url_q
#    return (url_q,tags_set)#返回一个存着全部标签页地址到队列 和 set
"""
    函数原型
    get_moviesurl_bytags(传入URL队列)
"""
if __name__ == "__main__":
    print ('This is main of module "step1.py"')
    get_tags_url_toRedis()
###结果直接保存在redis中  进行持久化
