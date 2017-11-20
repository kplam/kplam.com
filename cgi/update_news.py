#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:20:00 2017
"
@author: kplam
"""
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
from package.get import localconn
import random

# ===================
conn = localconn()

# ===================set requests================== #
rqs = rq.session()
rqs.keep_alive = False
rqshead = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
# ================================================= #
pages = range(1,2)
url = "http://kuaixun.stcn.com/index_%s.shtml"
# ip_list =pd.read_csv('ip.csv')['ip'].values
# ip = random.choice(ip_list)
# proxies = {"http": ip}
urllist = [url%(page_id) for page_id in pages]
newsresult = pd.DataFrame()
source ='stcn.com'
def get_news(url):
    html = rq.get(url,rqshead).content#,proxies=proxies).content
    # print(news.decode('utf-8'))
    newsSoup = bs(html, 'html.parser')
    newslist = newsSoup.select(".mainlist")
    newslist = bs(str(newslist[0]),'html.parser')
    newslist = newslist.find_all("p")
    result = []
    for i in range(len(newslist)):
        news = str(newslist[i])
        type = bs(news,'html.parser').a.text
        content = bs(news,'html.parser').a.next_element.next_element.text
        link = bs(news,'html.parser').a.next_element.next_element.attrs['href']
        datetime = str(bs(news,'html.parser').span.text)[1:20]
        result.append((source,type,content,link,datetime))

    result = pd.DataFrame(result,columns=['source','type','content','link','datetime'])
    result['datetime'] = result['datetime'].astype('datetime64[ns]')
    return result
sql_lastupdate = "SELECT * FROM `news` ORDER BY `news`.`datetime` DESC limit 0,1"
lastupdate = pd.read_sql(sql_lastupdate,conn)['datetime'].values[0]
print(lastupdate)
for i in range(len(urllist)):
    # names =globals()
    # names["p"+str(i)] = multiprocessing.Process(target=get_news(urllist[i],newsresult))
    # names["p"+str(i)].start()
    # names["p"+str(i)].join()
    result = get_news(urllist[i])
    newsresult = pd.concat((result,newsresult),ignore_index=True)

newsresult = newsresult[newsresult['datetime']>=lastupdate]
errorlist = []
for i in range(len(newsresult)):
    try:
        type = newsresult.get_value(i,'type')
        content = newsresult.get_value(i,'content')
        link = newsresult.get_value(i,'link')
        datetime = newsresult.get_value(i,'datetime')
        sql_update = "insert ignore INTO `news`(`source`, `type`, `content`, `link`, `datetime`) VALUES ('%s','%s','%s','%s','%s')"%(source,type,content,link,datetime)
        cur = conn.cursor()
        cur.execute(sql_update)
        conn.commit()
    except Exception as e:
        print(e)
        errorlist.append(e)
