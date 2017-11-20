# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:20:00 2017

@author: kplam
"""

import pymysql
import pandas as pd
import numpy as np


def conn(server,user,password):
    ser = server
    ur = user
    pw = password
    return pymysql.connect(host=ser,port=3306,user=ur,password=pw,db='stockdata',charset='utf8')

def localconn():
    return conn("192.168.1.111","root","1")

def get_df_stocklist():
    conn = localconn()
    sqlcode = "SELECT * FROM `stocklist` WHERE 1;"
    list = pd.read_sql(sqlcode, conn)
    return list

def get_stocklist():
    list = get_df_stocklist()
    list = np.array(list['证券代码'])
    list = list.tolist()
    return list

def get_stocklist_prefix(SH,SZ,pre=1):
    """
    :param SH: 第一参数为上海前/后缀
    :param SZ: 第二参数为深圳前/后缀
    :param PRE:前缀为1,后缀为0
    :return:
    """
    list = get_df_stocklist()
    pflist = []
    for i in range(len(list)):
        symbol = list.get_value(i, '证券代码')
        if pre:
            if symbol[0] == "6":
                pflist.append(SH+symbol)
            else:
                pflist.append(SZ+symbol)
        else:
            if symbol[0] == "6":
                pflist.append(symbol+SH)
            else:
                pflist.append(symbol+SZ)
    return pflist

def get_df_basedata():
    conn = localconn()
    sqlcode = "SELECT * FROM `basedata` WHERE 1;"
    list = pd.read_sql(sqlcode, conn)
    return list

def get_df_indexlist():
    conn = pymysql.connect(host='192.168.1.111', port=3306, user='root', passwd='1',
                       db='stockdata', charset='utf8')
    sqlcode = "SELECT * FROM `indexlist` WHERE 1;"
    list = pd.read_sql(sqlcode, conn)
    return list

def get_indexlist():
    list = get_df_indexlist()
    list = np.array(list['code'])
    list = list.tolist()
    return list

def get_indexlist_prefix(SH,SZ,pre=1):
    """
    :param SH: 第一参数为上海前/后缀
    :param SZ: 第二参数为深圳前/后缀
    :param PRE:前缀为1,后缀为0
    :return:
    """
    list = get_df_indexlist()
    pflist = []
    for i in range(len(list)):
        symbol = list.get_value(i, 'code')
        if pre:
            if symbol[0] == "0":
                pflist.append(SH+symbol)
            else:
                pflist.append(SZ+symbol)
        else:
            if symbol[0] == "0":
                pflist.append(symbol+SH)
            else:
                pflist.append(symbol+SZ)
    return pflist

def realtime(code):
    # ===================set requests================== #
    rqs = rq.session()
    rqs.keep_alive = False
    rqshead = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    # ===================get requests================== #
    urlsina = "http://hq.sinajs.cn/list=%s"%(code)
    lastbar = str(rq.get(urlsina,headers=rqshead).content)
    # ===================data processing================== #
    dayline = []
    for i in ('_','=','sz','sh'):
        lastbar = lastbar.replace(i,',')
    lastbar_sp =lastbar.split(',')
    dayline.append(lastbar_sp)
    dayline = pd.DataFrame(dayline,columns=['a','b','c','code','d','open','preclose','close','high','low','e','f','vol','amo','g','h','I','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','date','aa','ab'])
    if dayline.get_value(0,'ab')[0:2]=='00':
        dailybar_dtype = dayline.loc[:,['code','date','open','close','high','low','vol','amo','preclose']]
        dailybar_dtype['date'] = dailybar_dtype['date'].astype('datetime64')
        dailybar_dtype['close'] = dailybar_dtype['close'].astype('float32')
        dailybar_dtype['high'] = dailybar_dtype['high'].astype('float32')
        dailybar_dtype['low'] = dailybar_dtype['low'].astype('float32')
        dailybar_dtype['open'] = dailybar_dtype['open'].astype('float32')
        dailybar_dtype['vol'] = dailybar_dtype['vol'].astype('float32')
        dailybar_dtype['amo'] = dailybar_dtype['amo'].astype('float32')
        dailybar = dailybar_dtype[dailybar_dtype['vol']>0]
    else:
        dailybar = pd.DataFrame()
    return dailybar

if __name__== "__main__":
    list = get_df_stocklist()

    print(list)
