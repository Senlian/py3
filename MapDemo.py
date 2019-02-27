#!/usr/bin/env python
# encoding: utf-8

'''

@author: senlian

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@file: MapDemo.py

@time: 2019/1/11 16:41

@module:python -m pip install 

@desc:
'''


def sqr(item):
    return item * item

if __name__ == '__main__':
    objList = [1, 2, 3]
    newList = map(sqr, objList)
    print(newList)
    print(list(newList))
    print([sqr(item) for item in objList])
