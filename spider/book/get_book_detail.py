#!/usr/bin/env python
# encoding: utf-8

"""
@version: python2.7
@author: ‘sen-ele‘
@license: Apache Licence 
@file: get_book_detail
@time: 16/4/17 PM2:01
"""
from bs4 import BeautifulSoup
from redis import Redis
import requests as paw
import re
from pymongo import MongoClient
host="zp.tristan.pub"
port=10011
client=MongoClient(host=host,port=port)
r = Redis()
db = client.paw
import time
def get(url):

    mv=dict()

    response=paw.get(url)
    print "paw end!"

    if(response.status_code!=200):
        print(response.status_code)
        print("Exit from Exception")
        exit()
    try:
        soup_page=BeautifulSoup(response.text,'lxml')
        name=soup_page.find('span',property="v:itemreviewed").text
        mv_img=soup_page.find('a',class_='nbg')
        mv['info']=str(soup_page.find('div',id='info'))
        rating_num=soup_page.find('div',class_='rating_self clearfix').find('strong',class_='ll rating_num ')
        mv_id=re.search(r'[0-9].*[0-9]',url).group(0)
        mv['name']=name
        mv['img']=mv_img['href']
        mv['rating']=rating_num.text
        mv['id']=mv_id
    except Exception,e:
        print(url)
        print e
        raise "Raise a Exception in 解析详情页"

    return mv
def insert():

    while True:
        if r.scard("book_urls"):
            url=r.spop("book_urls")
            book = dict()
            book['type'] = "豆瓣书籍"
            book["tid"] = 2
            try:
                mv=get(url)
                book['id']=mv['id']
                book['content']=mv

                a = db.data.find_one({"id": book['id']})
                if (not a):
                    db.data.insert_one(book)
                    print("insert success")
                else:
                    print("Failed,id exist")
            except Exception,e:
                print(e)
                r.sadd("failed_book_url",url)
            time.sleep(1)
        else:
            print("All finished!")
            break
if __name__ == "__main__":
    insert()
