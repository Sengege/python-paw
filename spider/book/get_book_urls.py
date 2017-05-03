#!/usr/bin/env python
# encoding: utf-8

"""

"""
import requests as paw
from bs4 import BeautifulSoup
import re
from redis import Redis
import time
def get_now():
    now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    return now

r=Redis()

s = paw.session()
s.keep_alive = False
key="book_tags"
save_key="book_urls"

def get_onepage_urls(tag):
    response = paw.get(tag)
    if (response.status_code != 200):
        print(response.status_code)
        print get_now()
        r.lpush(key,tag)
        raise Exception("Exception throws")

    soup_page = BeautifulSoup(response.text, 'lxml')
    raw_urls = soup_page.find_all('a', href=re.compile('^https://book.douban.com/subject/[0-9].*[0-9]/$'))

    for temp in raw_urls:
        r.sadd(save_key, temp['href'])

    try:
        raw_total = soup_page.find('span', class_='thispage')
        nextpage = raw_total.find_next('a', href=re.compile('^/tag/.*type=T$'))['href']
        nextpage ="https://book.douban.com"+nextpage
    except:
        nextpage = 'EOF'
    return nextpage
def get_allpage_urls(tag):
    nextpage=tag
    while True:
        nextpage=get_onepage_urls(nextpage)
        print nextpage
        time.sleep(10)
        if "EOF"==nextpage:
            break

while r.scard(key):
    next_tag = r.spop(key)
    print next_tag
    get_allpage_urls(next_tag)