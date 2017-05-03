# -*- coding: utf-8 -*-
import requests as paw
from bs4 import BeautifulSoup
import re
from redis import Redis
r=Redis()
#传入一个标签的页面URL，
#和全局的储存电影页面的URL的set，返回该标签下一页的地址。
#当下一页地址不存在时候返回长度为0的str类型
def get_urls(url,movie):
    response=paw.get(url)#得到response响应的对象
    if(response.status_code!=200):
        print(response.status_code)
        raise Exception("Exception throws")
     
    soup_page=BeautifulSoup(response.text,'lxml')#转化字符串的网页源文件到Soup的page对象
    raw_urls=soup_page.find_all('a',href=re.compile('^https://movie.douban.com/subject/'))

    for temp in raw_urls:
        #将电影的地址加入集合
        #print(temp)
        #movies.add(temp['href'])
        #print(temp['href'])
        r.sadd('mv_set',temp['href'])
        r.lpush('mv_list',temp['href'])
    try:
        raw_total=soup_page.find('span',class_='thispage')
        total=int(raw_total['data-total-page'])
        #得到下一页的地址
        #"""!!!
        nextpage=raw_total.find_next('a',href=re.compile('^https://movie.douban.com/tag/.*type=T$'))['href']
    except:
        nextpage=''
    return nextpage
def get_movies_urls(url,movies):
    while(len(url)!=0):
        try:
            url=get_urls(url,movies)
            print(url)
        except:
            raise
