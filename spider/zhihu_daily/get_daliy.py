#!/usr/bin/env python
# encoding: utf-8

"""
@version: python2.7
@author: ‘sen-ele‘
@license: Apache Licence 
@file: get_daliy
@time: 16/4/17 AM1:59
"""
import requests as paw
from bs4 import BeautifulSoup as soup
import os
import json
url="http://news-at.zhihu.com/api/4/news/latest"
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
hd = {
    "User-Agent": agent,
    "Accept": "text/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

}
response=paw.get(url,headers=hd)
if(response.status_code!=200):
    print response.status_code
    os._exit()
news=json.loads(response.text)


print len(news['top_stories'])
print len(news['stories'])
# from pymongo import MongoClient
# host="zp.tristan.pub"
# port=10011
# client=MongoClient(host=host,port=port)
# db=client.paw
#
# story_base="http://news-at.zhihu.com/api/4/news/"
#
# for t in news['top_stories'],news['stories']:
#     for i in t:
#         story = dict()
#         story['type']="zhihu_daily"
#         story['tid']=3
#         story['id']=i['id']
#         story['date'] = news['date']
#         url=story_base+str(i['id'])
#         response = paw.get(url, headers=hd)
#         content = json.loads(response.text)
#         story['content']=content
#         db.data.insert_one(story)