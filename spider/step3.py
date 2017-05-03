from bs4 import BeautifulSoup
from redis import Redis
import requests as paw
import re
from pymongo import MongoClient
client = MongoClient()
db = client.douban
test='a'
def get(url):
    mv=dict()


    print(url)
    response=paw.get(url)

    if(response.status_code!=200):
        print(response.status_code)
        print("Exit from Exception")
        exit()
    try:
        soup_page=BeautifulSoup(response.text,'lxml')
        name=soup_page.find('span',property="v:itemreviewed").text
        year=soup_page.find('span',class_="year").text
        mv_info=soup_page.find('div',class_="indent clearfix")
        mv_img=mv_info.find('img',src=re.compile('^https://.*.doubanio.com/'))
        rating_num=soup_page.find('div',class_='rating_self clearfix').find('strong',class_='ll rating_num')
        mv_id=re.search(r'[0-9].*[0-9]',url).group(0)
        mv['name']=name
        mv['year']=year
        mv['img']=mv_img['src']
        print(rating_num.text)
        mv['rating']=float(rating_num.text)  #new modify to int for pick
        #mv['info']=mv_info
        mv['id']=mv_id
    except:
        print(url)
        print("Raise a Exception")
        pass

    return mv
def insert():
    r=Redis()
    url_list=r.lrange("mv_list",1400,1500)
    print(type(url_list))
    #raw_input()
    for url in url_list:
        mv=get(url)
        a=db.mv_test1.find_one({"id":mv['id']})
        if(not a):
            db.mv_test1.insert_one(mv)
            print("insert success")
        else:
            print("Failed,id exist")
if __name__ == "__main__":
    insert()
