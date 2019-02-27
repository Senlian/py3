#!/usr/bin/env python
# encoding: utf-8

'''

@author: senlian

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@file: Filter.py

@time: 2019/1/11 17:07

@module:python -m pip install 

@desc:
'''


def func(item):
    return item % 2 == 0


if __name__ == '__main__':
    objList = [1, 2, 3, 4, 5]
    print(filter(func, objList))
    print(list(filter(func, objList)))
    print(memoryview(bytearray(objList)))
    print(round(70.23456,3))
    c = (compile('print("a")','','eval'))
    eval(c)
