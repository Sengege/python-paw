# -*- coding: utf-8 -*-
import step1 as gtu
import step2 as gmu
import Queue
import os
from redis import Redis
r=Redis()

#得到所有豆瓣的电影标签的地址
#函数返回一个存有所有豆瓣电影标签地址的队列
#tags_queue=gtu.get_tags_url()
mset=set()
#print "tags_queue is Empyt:"+ str(tags_queue.empty())

while(r.llen('tag_urls')!=0):
    #从Redis得到tag的URL一个地址
    next_tagurl=r.rpop("tag_urls")
    #next_tagurl=tags_queue.get()
    print('开始新标签的抓取')
    print(next_tagurl)
    try:
        gmu.get_movies_urls(next_tagurl,mset)
    except:
        r.rpush("tag_urls",next_tagurl)
        print("Exit from Exception")
        exit()
