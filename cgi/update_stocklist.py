# -*- coding: utf-8 -*-
#!/usr/bin/env/ python3
"""
Created on Thu May  4 15:20:00 2017
"
@author: kplam
"""
import requests as rqs
import pandas as pd
import numpy as np
import re
import pymysql
import datetime
from package.function import *
from package.get import *

today = datetime.date.today()
print("今天是",today)

hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chr'
                    'ome/41.0.2272.118 Safari/537.36'}
conn = localconn()
stocklist = get_stocklist()
print("正在获取信息...")
get_url = rqs.get('http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=NS&sty=NSSTV5&st=12&sr=true&p=1&ps=100',headers = hea)
html_doc = str(get_url.content,'utf-8')
return_list = re.findall("\"(.*?)\"",get_url.text)
xgtable = []
for j in range(len(return_list)):
    appd = re.split(",",return_list[j])
    xgtable.append(appd)
xg = pd.DataFrame(xgtable)
xg = pd.DataFrame(np.array(xg[[3,4,10,13]]),columns=['name','code','ipoprice','ipodate'])
xg['ipodate'] = xg['ipodate'].astype('datetime64[ns]')
print("信息获取成功，正在写入数据库...")
Errorlist = []
for i in range(len(xg)):
    code = str(xg.get_value(i,'code'))
    name = xg.get_value(i,'name')
    pinyin = getpinyin(name)
    ipoprice = xg.get_value(i,'ipoprice')
    ipodate = xg.get_value(i,'ipodate')

    if code[0] == '6' :
        market = '上海证券交易所'
    else:
        market = '深圳证券交易所'

    if code in stocklist:
        print(code,":该股票已存在！")
    else:
        try:
            sql_sl = "INSERT INTO `stocklist`(`证券代码`, `证券简称`, `上市市场`,`拼音缩写`) VALUES('%s','%s','%s','%s')"%(code,name,market,pinyin)
            cur = conn.cursor()
            cur.execute(sql_sl)
            conn.commit()
            print(code,"：更新成功！")
        except Exception as e:
            print(code,"：更新失败！", e)
            Errorlist.append(code)

xg2 = xg.dropna()
xg2 = xg2[xg2['ipodate']>=today]
xg2 = np.array(xg2)
xg2 = pd.DataFrame(xg2,columns=['name','code','ipoprice','ipodate'])
for i in range(len(xg2)):
    code = xg2.get_value(i,'code')
    ipoprice = xg2.get_value(i,'ipoprice')
    ipodate = xg2.get_value(i,'ipodate')
    sql_bd="update `basedata` set `首发日期`='%s' ,`首发价格`='%s' WHERE `证券代码`='%s'"%(ipodate,ipoprice,code)
    try:
        cur = conn.cursor()
        cur.execute(sql_bd)
        conn.commit()
    except Exception as e:
        print(code, e)
        Errorlist.append(code)

dfErrorList = pd.DataFrame({'error': Errorlist})
dfErrorList.to_csv(path()+'/error/update_stocklist.csv')
print(dfErrorList)
