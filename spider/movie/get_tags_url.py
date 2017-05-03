#!/usr/bin/env python
# encoding: utf-8

"""
@version: python2.7
@author: ‘sen-ele‘
@license: Apache Licence 
@file: get_tags_url
@time: 16/4/17 AM12:27
"""

import requests as paw
from bs4 import BeautifulSoup
import re
import os
from redis import Redis

base = "https://movie.douban.com/tag/"  # 豆瓣标签地址
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
hd = {
    "Referer": "https://movie.spider.com/",
    "User-Agent": agent,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

}

r=Redis()

def get_tags_url():


    response=paw.get(url=base,headers=hd)
    soup_page=BeautifulSoup(response.text,'lxml')
    if(response.status_code!=200):
        print 'status_code: '+ str(response.status_code)
        os._exit()

    tags=soup_page.find_all('a',href=re.compile('^/tag'))



    for tag in tags:
        end_url=base+tag.text
        r.sadd("movie_tags", end_url)


if __name__ == "__main__":
    get_tags_url()