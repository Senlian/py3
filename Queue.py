#!/usr/bin/env python
# encoding: utf-8

'''

@author: senlian

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@file: Queue.py

@time: 2019/1/11 16:03

@module:python -m pip install 

@desc:
'''
import queue
from collections import deque


def yanghui(k):
    """
    :param k: 杨辉三角中第几层
    :return: 第K层的系数
    """
    q = deque([1])  # 创建一个队列，默认从1开始
    for i in range(k):  # 迭代要查找的层数
        for _ in range(i):  # 循环需要出队多少次
            a = q.popleft()
            b = q[0]
            q.append(a + b)  # 第一个数加上队列中第二个数并赋值到队列末尾
            # print(a,b, a+b, q)
        q.append(1)  # 每次查找结束后都需要在队列最右边添加个1
        print(list(q))
    return list(q)


if __name__ == '__main__':
    result = yanghui(4)
    print(result)
    from queue import Queue
    print(dir(Queue))
    from queue import LifoQueue
    from queue import PriorityQueue
    from collections import deque
    print(5//2)