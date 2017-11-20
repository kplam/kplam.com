#!/usr/bin/python3
#  -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:20:00 2017
"
@author: kplam
"""

import cgi, cgitb
import json
import datetime
import re
import talib
from package.get import *
from package.funcntion import *
from package.indicator import *
import numpy as np
import pandas as pd

# =========== Global define ============#

print("Content-type:application/json\n")
today = datetime.date.today()
sDate_b0 = today - datetime.timedelta(days=365)

# ========= URL Param =========== #

URL_param = cgi.FieldStorage()
sCode = URL_param.getvalue('code')
sDate_b = URL_param.getvalue('bdate')
sDate_e = URL_param.getvalue('edate')
sIndicator = URL_param.getvalue('ta')

# ========= URL Param Check ============= #

indexlist = get_dfindexlist()
if sCode in indexlist['code'].values:
    sCode = sCode
    sName = indexlist[indexlist['code']==sCode]
    sName = sName['name'].values[0]
else:
    sCode = indexlist['code'].values[0]
    sName = indexlist['name'].values[0]

if is_valid_date(sDate_b):
    sDate_b = sDate_b
else:
    sDate_b = str(sDate_b0)

if is_valid_date(sDate_e):
    sDate_e = sDate_e
else:
    sDate_e = str(today)

if str(sIndicator).strip() != "":
    try:
        list_indicator = re.split('\_',sIndicator)+['jl','js','macd']
        list_indicator = list(set(list_indicator))
    except:
        list_indicator = ['jl','js','macd']
else:
    list_indicator = ['jl','js','macd']

# ========== get sql data and calc adj ================== #

sqlcon = localconn()

sql_daybar = "Select * From `indexdb` WHERE `code`='%s' and `date` BETWEEN '%s' and '%s' " % (sCode, sDate_b, sDate_e)
DF_daybar = pd.read_sql(sql_daybar, sqlcon)
df = DF_daybar[['code', 'date', 'open', 'close', 'high', 'low', 'vol', 'amo']]

# ========== get realtime data ================== #

if sDate_e == str(today) and df.get_value(len(df)-1,'date')<today:
    if sCode[0] == "0":
        sCode_url = "sh"+sCode
    else:
        sCode_url = "sz"+sCode
    try:
        df_realtime = realtime(sCode_url)
        df_realtime = df_realtime[['code','date','open','close','high','low','vol','amo']]
        df = pd.concat([df,df_realtime],ignore_index=True)
    except:
        df = df

# ============== prepare for indicator calc =================#

db_date = df['date'].values
db_high = df['high'].values
db_open = df['open'].values
db_low = df['low'].values
db_close = df['close'].values
db_vol = df['vol'].values
db_amo = df['amo'].values

# ================= dailybar json output prepare =================== #

df['date'] = df['date'].astype(str)
df.index = df['date'].tolist()

json_daybar = df[['open', 'close', 'high', 'low']].to_json(orient="split")
dict_daybar = json.loads(json_daybar)
json_vol = df['vol'].to_json(orient="split")
dict_vol = json.loads(json_vol)
json_amo = df['amo'].to_json(orient="split")
dict_amo = json.loads(json_amo)
dict_daybar["vol"] = dict_vol["data"]
dict_daybar["amo"] = dict_amo["data"]
dict_daybar["name"] = sName
dict_daybar["code"] = sCode

# ================= indicator calc ========================= #

sql_indicator = "select * from `indicator`"
df_indicator = pd.read_sql(sql_indicator,sqlcon)
available_indicator = df_indicator['short'].values
indicator_main = []
indicator_sub = []
for i in range(len(list_indicator)):
    names = locals()
    if list_indicator[i] in available_indicator:
        if df_indicator[df_indicator['short'] == list_indicator[i]]['main'].values[0] == 1:
            indicator_main.append((list_indicator[i] + ":" +
                                   df_indicator[df_indicator['short'] == list_indicator[i]]['output'].values[0]))
        else:
            indicator_sub.append((list_indicator[i] + ":" +
                                  df_indicator[df_indicator['short'] == list_indicator[i]]['output'].values[0]))
        name_indicator = list_indicator[i]
        name_indicator = list_indicator[i]
        df_ind_pram = df_indicator[df_indicator['short'] == name_indicator]
        pram_input = df_ind_pram['input'].values[0]
        pram_output = df_ind_pram['output'].values[0]
        pram_input = re.split("\,",pram_input)
        pram_output = re.split("\,",pram_output)
        lstPram = []
        for sPram in pram_input:
            lstPram.append(globals()[sPram])    # 报错说明全局中没有该名字的变量
        if len(pram_output) > 1:
            for j in range(len(pram_output)):
                name_output = pram_output[j]
                df[name_output] = names[name_indicator](*lstPram)[j]    # 名字要按顺序存入数据库
                names['json_'+name_output] = df[name_output].round(4).to_json(orient="split")
                names['dict_'+name_output] = json.loads(names['json_'+name_output])
                dict_daybar[name_output] = names['dict_'+name_output]["data"]
        else:
            for j in range(len(pram_output)):
                name_output = pram_output[j]
                df[name_output] = names[name_indicator](*lstPram)
                names['json_'+name_output] = df[name_output].round(4).to_json(orient="split")
                names['dict_'+name_output] = json.loads(names['json_'+name_output])
                dict_daybar[name_output] = names['dict_'+name_output]["data"]

# ================== json output ================#
dict_daybar['main'] = indicator_main
dict_daybar['sub'] = indicator_sub
dict_daybar['dates'] = dict_daybar['index']
del dict_daybar['index']
dict_daybar['OCHL'] = dict_daybar["data"]
del dict_daybar['data']
del dict_daybar['columns']
json_output = json.dumps(dict_daybar,sort_keys=True,indent=4)
print(json_output)


