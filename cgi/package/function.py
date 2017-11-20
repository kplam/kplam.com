# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:20:00 2017

@author: kplam
"""

import os
import sys
import datetime

def IsValidFloat(sFloat):
    try:
        f = float(sFloat)
        return f
    except:
        return False


def IsSubString(SubStrList, Str):
    for substr in SubStrList:
        if not (substr in Str):
            return False
    return True

def GetFileList(FindPath, FlagStr=None):
    FileList = []
    FileNames = os.listdir(FindPath)

    if not len(FileNames):
        return

    if not FlagStr:
        for fn in FileNames:
            fullfilename = os.path.join(FindPath, fn)
            FileList.append(fullfilename)
        return FileList

    for fn in FileNames:
        if IsSubString(FlagStr, fn):
            fullfilename = os.path.join(FindPath, fn)
            FileList.append(fullfilename)

    return FileList

def path():
    return os.path.abspath(os.path.dirname(sys.argv[0]))

def txt_pre(s):
    txtstr = s
    txt_d=txtstr.replace('%','%%')
    return txt_d
    
def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'A'
        if asc >= -20283 and asc <= -19776:
            return 'B'
        if asc >= -19775 and asc <= -19219:
            return 'C'
        if asc >= -19218 and asc <= -18711:
            return 'D'
        if asc >= -18710 and asc <= -18527:
            return 'E'
        if asc >= -18526 and asc <= -18240:
            return 'F'
        if asc >= -18239 and asc <= -17923:
            return 'G'
        if asc >= -17922 and asc <= -17418:
            return 'H'
        if asc >= -17417 and asc <= -16475:
            return 'J'
        if asc >= -16474 and asc <= -16213:
            return 'K'
        if asc >= -16212 and asc <= -15641:
            return 'L'
        if asc >= -15640 and asc <= -15166:
            return 'M'
        if asc >= -15165 and asc <= -14923:
            return 'N'
        if asc >= -14922 and asc <= -14915:
            return 'O'
        if asc >= -14914 and asc <= -14631:
            return 'P'
        if asc >= -14630 and asc <= -14150:
            return 'Q'
        if asc >= -14149 and asc <= -14091:
            return 'R'
        if asc >= -14090 and asc <= -13119:
            return 'S'
        if asc >= -13118 and asc <= -12839:
            return 'T'
        if asc >= -12838 and asc <= -12557:
            return 'W'
        if asc >= -12556 and asc <= -11848:
            return 'X'
        if asc >= -11847 and asc <= -11056:
            return 'Y'
        if asc >= -11055 and asc <= -10247:
            return 'Z'
        return ''

def getpinyin(string):
    if string == None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        try:
            charLst.append(single_get_first(l).decode('utf-8'))
        except:
            charLst.append(single_get_first(l))
    return ''.join(charLst)
