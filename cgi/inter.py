#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:20:00 2017
"
@author: kplam
"""

import cgi, cgitb
import pymysql
import json
import pandas as pd
import numpy as np
import re
import datetime
from package.get import *
from package.function import *

# cgitb.enable()

# =========== Global define ================ #

print("Content-type:application/json\n")
today = datetime.date.today()
conn = localconn()
sql_reportdate = "select distinct `报表日期` from faresult ORDER BY `报表日期` DESC"
list_reportdate = pd.read_sql(sql_reportdate, conn)

# ============= Url Param ================== #

url_param = cgi.FieldStorage()
url_date = url_param.getvalue('date')
url_type = url_param.getvalue('type')
url_amorank = url_param.getvalue('ar1')
url_araise = url_param.getvalue('ar2')
url_model = url_param.getvalue('tamodel')
url_report = url_param.getvalue('quarter')
url_weight = url_param.getvalue('qweight')
url_wcompare = url_param.getvalue('wcompare')
url_inter = url_param.getvalue('inter')

# ============= param check ================ #

if is_valid_date(url_date):
    sDate = url_date
else:
    sDate = today

if str(url_type).strip() != "":
    try:
        list_type = re.split('\_', url_type)
    except:
        list_type = 0
else:
    list_type = 0

if url_amorank != "":
    try:
        if IsValidInt(url_amorank):
            iAmoRank = int(url_amorank)
        else:
            iAmoRank = 500
    except:
        iAmoRank = 500
else:
    iAmoRank = 500

if url_araise != "":
    try:
        if IsValidInt(url_araise):
            iARaise = int(url_araise)
        else:
            iARaise = -100
    except:
        iARaise = -100
else:
    iARaise = -100

if url_model != "":
    try:
        if int(url_model) in range(1, 10):
            sModel = url_model
        else:
            sModel = '0'
    except:
        sModel = '0'
else:
    sModel = '0'

if url_report != "":
    try:
        if int(url_report) in range(len(list_reportdate)):
            iQuarter = url_report
            sReportdate = str(list_reportdate.get_value(int(url_report) + 1, '报表日期'))
        else:
            iQuarter = 12
            sReportdate = str(list_reportdate.get_value(12, '报表日期'))
    except:
        iQuarter = 12
        sReportdate = str(list_reportdate.get_value(12, '报表日期'))
else:
    iQuarter = 12
    sReportdate = str(list_reportdate.get_value(12, '报表日期'))

if url_weight != "":
    if IsValidFloat(url_weight):
        sWeight = float(url_weight)
    else:
        sWeight = 0.8
else:
    sWeight = 0.8

if url_wcompare != "":
    if IsValidFloat(url_wcompare):
        swcompare = float(url_wcompare)
    else:
        swcompare = 0.4
else:
    swcompare = 0.4

if str(url_inter).strip() != "":
    try:
        list_inter = re.split('\_', url_inter)
    except:
        list_inter = 0
else:
    list_inter = 0

# ============ calc weight =========== #

weight = []
for i in range(len(list_reportdate)):
    reportdate = list_reportdate.get_value(i, '报表日期')
    weight.append((reportdate, 1 * sWeight ** i))
weight = pd.DataFrame(weight, columns=['报表日期', 'weight'])
weight = weight[:iQuarter]

# ============ SQL query =================== #

sql_AmoRank = "Select `code` from `usefuldata` WHERE `AmoRank`<'%s' and `ARaise`<'%s' and `date`='%s'" % (
iAmoRank, iARaise, sDate)
sql_indicator = "Select `code` from `usefuldata` where `date`='%s' and `taresult` LIKE '%%%s%%'" % (sDate, sModel)
sql_FA = "Select * from `faresult` WHERE `报表日期`>'%s' ORDER BY `报表日期` DESC " % (sReportdate)

# =============== get data ================ #

DF_AmoRank = pd.read_sql(sql_AmoRank, conn)
DF_indicator = pd.read_sql(sql_indicator, conn)
DF_FA = pd.read_sql(sql_FA, conn)

# ============== data process ============== #

fa_result = pd.merge(DF_FA, weight)
fa_result = fa_result['weight'].groupby(fa_result['代码']).sum()
fa_result = fa_result.reset_index().sort_values(by=['weight'], ascending=False)
list_FA = fa_result[fa_result.weight > weight['weight'].sum() * swcompare]['代码'].values
list_indicator = DF_indicator['code'].values
list_AmoRank = DF_AmoRank['code'].values

# ================= output ================= #

dict_output = {}
if list_type != 0:
    for stype in list_type:
        if stype == 'ta' and sModel != 0:
            json_ta = DF_indicator['code'].to_json(orient="split")
            dict_ta = json.loads(json_ta)
            dict_output['ta'] = dict_ta["data"]
        elif stype == 'fa':
            df_faoutput = pd.DataFrame(list_FA, columns=['code'])
            json_fa = df_faoutput['code'].to_json(orient="split")
            dict_fa = json.loads(json_fa)
            dict_output['fa'] = dict_fa["data"]
        elif stype == 'amo':
            json_amo = DF_AmoRank['code'].to_json(orient="split")
            dict_amo = json.loads(json_amo)
            dict_output['amo'] = dict_amo["data"]
        else:
            dict_output['empty'] = True
else:
    dict_output['empty'] = True

# =============== intersection =============== #

names = globals()
if list_inter != 0:
    ta = list_indicator
    fa = list_FA
    amo = list_AmoRank
    if len(list_inter) == 2:
        try:
            list_output = list(set(names[list_inter[0]]).intersection(set(names[list_inter[1]])))
        except:
            list_output = []
    elif len(list_inter) == 3:
        try:
            list_output01 = list(set(names[list_inter[0]]).intersection(set(names[list_inter[1]])))
            list_output = list(set(list_output01).intersection(set(names[list_inter[2]])))
        except:
            list_output = []
    else:
        list_output = []
else:
    list_output = []

if len(list_output) != 0:
    DF_inter = pd.DataFrame(list_output, columns=['code'])
    json_inter = DF_inter['code'].to_json(orient="split")
    dict_inter = json.loads(json_inter)
    dict_output['inter'] = dict_inter["data"]
else:
    dict_output['inter'] = "empty!"

# =============== json_output =============== #

json_output = json.dumps(dict_output)
print(json_output)
