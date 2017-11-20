#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:20:00 2017
"
@author: kplam
"""
import talib
import numpy as np
import pandas as pd
from numpy import NaN
from math import isnan

def macd(close):
    """
    MACD
    :param close: price list
    :return: diff, dea, hist(3 columns)
    """
    diff, dea, hist = talib.MACD(close,fastperiod=12, slowperiod=26, signalperiod=9)
    return diff, dea, hist

def sma(close,N,M):
    """
    SMA
    :param close: price list
    :param N: period
    :param M: weight
    :return: sma list(1 columns)
    """
    List_sma = []
    for i in range(len(close)):
        if i == 0:
            iSMA = close[0]
            List_sma.append(iSMA)
        else:
            if isnan(List_sma[i-1]) == False :
                iSMA = (close[i]*M+(List_sma[i-1])*(N-M))/N
            else:
                iSMA = close[i]
            List_sma.append(iSMA)
    List_sma = pd.DataFrame(List_sma)
    return List_sma

def ref(close,N):
    List_ref =[]
    for i in range(len(close)):
        if i == 0:
            fref = NaN
        elif i < N :
            fref = NaN
        else:
            fref = close[i-N]
        List_ref.append(fref)
    List_ref = pd.DataFrame(List_ref)
    return List_ref

def rsi(close):
    rsi6 = talib.RSI(close,timeperiod=6)
    rsi12 = talib.RSI(close,timeperiod=12)
    rsi24 = talib.RSI(close,timeperiod=24)
    return rsi6,rsi12,rsi24

def boll(close):
    return talib.BBANDS(close,timeperiod=26,nbdevup=2,nbdevdn=2)

def kdj(close,high,low):
    k,d =talib.STOCH(high=high,low=low,close=close,fastk_period=9,slowk_period=3,slowd_period=3)
    j =3*k-2*d
    return k, d, j

def adx(close,high,low):
    ladx = talib.ADX(high,low,close,timeperiod=14)
    ladxr =talib.EMA(ladx,6)
    return ladx,ladxr

def cci(close,high,low):
    return talib.CCI(high,low,close,timeperiod=14)

def obv(close,vol):
    return talib.OBV(close,vol)

def atr(close,high,low):
    return talib.NATR(high,low,close,timeperiod=14)

def ma(close):
    ma5 = talib.MA(close,timeperiod=5)
    ma10 = talib.MA(close, timeperiod=10)
    ma20 = talib.MA(close, timeperiod=20)
    ma60 = talib.MA(close, timeperiod=60)
    return ma5, ma10, ma20, ma60

def ema(close):
    ema5 = talib.EMA(close,timeperiod=5)
    ema10 = talib.EMA(close, timeperiod=10)
    ema20 = talib.EMA(close, timeperiod=20)
    ema60 = talib.EMA(close, timeperiod=60)
    return ema5, ema10, ema20, ema60

if __name__ == "__main__":
    print("Content-type:text/html\n")
    print("error!")
