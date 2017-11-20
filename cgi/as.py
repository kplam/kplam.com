#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:20:00 2017
"
@author: kplam
"""

import cgi, cgitb
import json
import datetime
import re
from package.get import *
from package.function import *
from package.indicator import *
import numpy as np
import pandas as pd

#cgitb.enable()

# =========== Global define ============#
Tstart = datetime.datetime.now()
print("Content-type:application/json\n")
today = datetime.date.today()
sDate_b0 = today - datetime.timedelta(days=365)

# ========= URL Param =========== #

URL_param = cgi.FieldStorage()
sCode = URL_param.getvalue('code')
# sCode = '600000'
sDate_b = URL_param.getvalue('bdate')
sDate_e = URL_param.getvalue('edate')
sAdjcump = URL_param.getvalue('adj')
sIndicator = URL_param.getvalue('ta')

# ========= URL Param Check ============= #

stocklist = get_dfstocklist()

if sCode in stocklist['证券代码'].values:
    sCode = sCode
    sName = stocklist[stocklist['证券代码'] == sCode]
    sName = sName['证券简称'].values[0]
else:
    sCode = stocklist['证券代码'].values[0]
    sName = stocklist['证券简称'].values[0]
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
        list_indicator = re.split('\_', sIndicator) + ['jl', 'js', 'macd']
        list_indicator = list(set(list_indicator))
    except:
        list_indicator = ['jl', 'js', 'macd']
else:
    list_indicator = ['jl', 'js', 'macd']

# ========== get realtime data ================#

if sCode[0] == "6":
    sCode_url = "sh" + sCode
else:
    sCode_url = "sz" + sCode

DF_realtime = realtime(sCode_url)

# ========== get sql data and calc adj ================== #

sqlcon = localconn()

sql_daybar = "Select * From `dayline` WHERE `code`='%s' and `date` BETWEEN '%s' and '%s' " % (sCode, sDate_b, sDate_e)
DF_daybar = pd.read_sql(sql_daybar, sqlcon)

if DF_daybar.empty == False or DF_realtime.empty == False:
    if sAdjcump != 'False':
        sql_split = "select * from `ftsplit` WHERE `code`='%s'and `date` BETWEEN '%s'and '%s'ORDER BY 'date' DESC " % (
        sCode, sDate_b, sDate_e)
        DF_split = pd.read_sql(sql_split, sqlcon)

        # ========== concat realtime data ================== #

        if sDate_e == str(today) and DF_daybar.get_value(len(DF_daybar) - 1, 'date') < today and comparetime():
            try:
                preclose = float(DF_daybar.get_value(len(DF_daybar) - 1, 'close'))
                adjpreclose = float(DF_realtime.get_value(0, 'preclose'))
                preadjfactor = DF_daybar.get_value(len(DF_daybar) - 1, 'adjfactor')
                preadjcump = DF_daybar.get_value(len(DF_daybar) - 1, 'adjcump')
                rt_adjfactor = preclose / adjpreclose
                rt_adjcump = preadjcump * rt_adjfactor
                if rt_adjfactor == 1:
                    DF_realtime['adjfactor'] = [preadjfactor]
                else:
                    DF_realtime['adjfactor'] = [rt_adjfactor]
                DF_realtime['adjcump'] = [rt_adjcump]
                DF_realtime = DF_realtime[
                    ['code', 'date', 'open', 'close', 'high', 'low', 'vol', 'amo', 'adjfactor', 'adjcump']]
                DF_daybar = pd.concat([DF_daybar, DF_realtime], ignore_index=True)
                DF_daybar['date'] = DF_daybar['date'].astype('datetime64')
                DF_split['date'] = DF_split['date'].astype('datetime64')
            except:
                DF_daybar = DF_daybar
        elif sDate_e == str(today) and DF_daybar.get_value(len(DF_daybar) - 1, 'date') == today and comparetime():
            try:
                preclose = float(DF_daybar.get_value(len(DF_daybar) - 2, 'close'))
                adjpreclose = float(DF_realtime.get_value(0, 'preclose'))
                preadjfactor = DF_daybar.get_value(len(DF_daybar) - 2, 'adjfactor')
                preadjcump = DF_daybar.get_value(len(DF_daybar) - 2, 'adjcump')
                rt_adjfactor = preclose / adjpreclose
                rt_adjcump = preadjcump * rt_adjfactor
                if rt_adjfactor == 1:
                    DF_realtime['adjfactor'] = [preadjfactor]
                else:
                    DF_realtime['adjfactor'] = [rt_adjfactor]
                DF_realtime['adjcump'] = [rt_adjcump]
                DF_realtime = DF_realtime[
                    ['code', 'date', 'open', 'close', 'high', 'low', 'vol', 'amo', 'adjfactor', 'adjcump']]
                DF_daybar = DF_daybar[:len(DF_daybar) - 1]
                DF_daybar = pd.concat([DF_daybar, DF_realtime], ignore_index=True)
                DF_daybar['date'] = DF_daybar['date'].astype('datetime64')
                DF_split['date'] = DF_split['date'].astype('datetime64')
            except:
                DF_daybar = DF_daybar
        else:
            DF_daybar = DF_daybar

        # ============= adjfactor ================= #

        if len(DF_daybar) > 20:
            if DF_daybar.empty == True:
                df = DF_daybar
            else:
                adjcump = DF_daybar.get_value(len(DF_daybar) - 1, 'adjcump')
                List_pre = []
                for j in range(len(DF_daybar)):
                    high = round45(DF_daybar.get_value(j, 'high') / (adjcump / DF_daybar.get_value(j, 'adjcump')))
                    open = round45(DF_daybar.get_value(j, 'open') / (adjcump / DF_daybar.get_value(j, 'adjcump')))
                    low = round45(DF_daybar.get_value(j, 'low') / (adjcump / DF_daybar.get_value(j, 'adjcump')))
                    close = round45(DF_daybar.get_value(j, 'close') / (adjcump / DF_daybar.get_value(j, 'adjcump')))
                    vol = DF_daybar.get_value(j, 'vol')
                    date = DF_daybar.get_value(j, 'date')
                    for k in range(len(DF_split)):
                        date_split = DF_split.get_value(k, 'date')
                        split = DF_split.get_value(k, '红股')
                        if date < date_split:
                            vol = vol * (1 + split / 10)
                        else:
                            vol = vol * 1
                    List_pre.append((sCode, date, high, open, low, close, vol, DF_daybar.get_value(j, 'amo'),
                                     DF_daybar.get_value(j, 'adjfactor'), DF_daybar.get_value(j, 'adjcump')))
                df = pd.DataFrame(List_pre,
                                  columns=['code', 'date', 'high', 'open', 'low', 'close', 'vol', 'amo', 'adjfactor',
                                           'adjcump'])
                df = df[['code', 'date', 'open', 'close', 'high', 'low', 'vol', 'amo']]
        else:
            df = DF_daybar[['code', 'date', 'open', 'close', 'high', 'low', 'vol', 'amo']]
    else:
        df = DF_daybar[['code', 'date', 'open', 'close', 'high', 'low', 'vol', 'amo']]

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
    dict_daybar["code"] = sCode
    dict_daybar["name"] = sName

    # ================= indicator calc ========================= #

    sql_indicator = "select * from `indicator`"
    df_indicator = pd.read_sql(sql_indicator, sqlcon)
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
            df_ind_pram = df_indicator[df_indicator['short'] == name_indicator]
            pram_input = df_ind_pram['input'].values[0]
            pram_output = df_ind_pram['output'].values[0]
            pram_input = re.split("\,", pram_input)
            pram_output = re.split("\,", pram_output)
            lstPram = []
            for sPram in pram_input:
                lstPram.append(globals()[sPram])  # 报错说明全局中没有该名字的变量
            if len(pram_output) > 1:
                for j in range(len(pram_output)):
                    name_output = pram_output[j]
                    df[name_output] = names[name_indicator](*lstPram)[j]  # 名字要按顺序存入数据库
                    names['json_' + name_output] = df[name_output].round(4).to_json(orient="split")
                    names['dict_' + name_output] = json.loads(names['json_' + name_output])
                    dict_daybar[name_output] = names['dict_' + name_output]["data"]
            else:
                for j in range(len(pram_output)):
                    name_output = pram_output[j]
                    df[name_output] = names[name_indicator](*lstPram)
                    names['json_' + name_output] = df[name_output].round(4).to_json(orient="split")
                    names['dict_' + name_output] = json.loads(names['json_' + name_output])
                    dict_daybar[name_output] = names['dict_' + name_output]["data"]


                    # ================== json output ================#
    dict_daybar['dates'] = dict_daybar['index']
    del dict_daybar['index']
    dict_daybar['OCHL'] = dict_daybar["data"]
    del dict_daybar['data']
    del dict_daybar['columns']
    dict_daybar['main'] = indicator_main
    dict_daybar['sub'] = indicator_sub
    json_output = json.dumps(dict_daybar, sort_keys=True, indent=4, ensure_ascii=False)
else:
    json_output = {"empty!"}
print(json_output)
