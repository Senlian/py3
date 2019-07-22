#!/usr/bin/env python
# encoding: utf-8

'''

@author: senlian

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@file: ComponentID.py

@time: 2018/12/26 8:54

@module:python -m pip install 

@desc:
'''
import wx, os, hashlib

# wx.NewId() 被替换成wx.NewIdRef()
ID_C_Root = wx.NewIdRef()
ID_C_HomePage = wx.NewIdRef()

ID_C_SIP = wx.NewIdRef()
ID_C_SPort = wx.NewIdRef()
ID_C_SUser = wx.NewIdRef()
ID_C_SKey = wx.NewIdRef()
ID_C_BtnCnt = wx.NewIdRef()

ID_C_IP = wx.NewIdRef()
ID_C_PkgID = wx.NewIdRef()
ID_C_SvcType = wx.NewIdRef()
ID_C_PkgType = wx.NewIdRef()

ID_C_SrcFile = wx.NewIdRef()
ID_C_BtnOpenFile = wx.NewIdRef()
ID_C_BtnSrc = wx.NewIdRef()
ID_C_BtnUpdate = wx.NewIdRef()
ID_C_Windows = wx.NewIdRef()
ID_C_MAC = wx.NewIdRef()
ID_C_Android = wx.NewIdRef()
ID_Ios = wx.NewIdRef()
ID_C_SubDir = wx.NewIdRef()

ID_C_BtnSwitch = wx.NewIdRef()
ID_C_TeLog = wx.NewIdRef()


def isfile(target):
    try:
        return os.path.isfile(target)
    except:
        return False


def get_md5(target):
    obj = hashlib.md5()
    if not isfile(target):
        if not isinstance(target, bytes):
            target = target.encode("utf-8")
        obj.update(target)
    else:
        with open(target, 'rb') as f:
            obj.update(f.read())
    return obj.hexdigest()


if __name__ == '__main__':
    pass
