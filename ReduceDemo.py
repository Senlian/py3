#!/usr/bin/env python
# encoding: utf-8

'''

@author: senlian

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@file: ReduceDemo.py

@time: 2019/1/11 16:52

@module:python -m pip install 

@desc:
'''
from functools import reduce


def add(x, y):
    return x + y

if __name__ == '__main__':
    objList = [1, 2, 3, 4]
    print(reduce(add, objList))
    print(reduce(add, objList, 20))
