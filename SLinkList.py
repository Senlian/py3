#!/usr/bin/env python
# encoding: utf-8

'''

@author: senlian

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@file: SLinkList.py

@time: 2019/1/11 9:39

@module:python -m pip install 

@desc:
'''


# TODO: 定义单向链表节点
class Node(object):
    def __init__(self, item=None):
        '''
        :param item: 记录当前节点值
        :param next: 记录下一个节点
        :return: None
        '''
        self.item = item
        self.next = None

    def __repr__(self):
        return repr(self.item)


# TODO: 定义单向链表
class SLinkList(object):
    def __init__(self):
        '''
        :param head: 头节点
        :param last: 尾节点
        :param length: 链表长度
        :return:
        '''
        self.head = None
        self.last = None
        self.curNode = None
        self.length = 0
        self.index = 0

    # 显示内容
    def __repr__(self):
        return repr(self.view())

    # 获取链表长度，适用len方法
    def __len__(self):
        '''
        count = 0
        curNode = self.head
        while curNode:
            count += 1
            curNode = curNode.next
        return count
        '''
        return self.length

    # 使链表可索引和切片
    def __getitem__(self, index):
        print(type(index))
        try:
            return self.view()[index]
        except IndexError as e:
            raise e

    # 标示可迭代
    def __iter__(self):
        return self

    # 适用next方法，实现可迭代
    def __next__(self):
        if not self.head or self.index >= self.length:
            raise StopIteration
        else:
            if not self.curNode:
                self.curNode = self.head
            curItem = self.curNode.val
            self.curNode = self.curNode.next
            self.index += 1
        return curItem

    # 判断链表是否为空
    def isEmpty(self):
        return self.head is None

    # 头部添加节点
    def add(self, item):
        newNode = Node(item)
        if self.isEmpty():
            self.head = newNode
            self.last = newNode
        else:
            newNode.next = self.head
            self.head = newNode
        self.length += 1
        return self

    # 尾部添加节点
    def append(self, item):
        newNode = Node(item)
        if self.isEmpty():
            self.head = newNode
        else:
            self.last.next = newNode
        self.last = newNode
        self.length += 1
        return self

    # 指定位置插入节点
    def insert(self, pos, item):
        if pos <= 0:
            self.add(item)
        elif pos >= self.length:
            self.append(item)
        else:
            newNode = Node(item)
            curNode = self.head
            count = 0
            while count != pos:
                count += 1
                preNode = curNode
                curNode = curNode.next
            preNode.next = newNode
            newNode.next = curNode
            self.length += 1
        return self

    # 删除元素
    def remove(self, item):
        if self.isEmpty() or not self.find(item):
            return self
        else:
            curNode = self.head
            curItem = curNode.item
            if curItem == item and self.length == 1:
                self.head = None
                self.last = None
            elif curItem == item and self.length > 1:
                self.head = curNode.next
            else:
                while item != curItem:
                    preNode = curNode or None
                    curNode = curNode.next or None
                    nextNode = None if not curNode else curNode.next
                    curItem = None if not curNode else curNode.item
                preNode.next = nextNode
            self.length -= 1

    # 查找元素，返回元素节点
    def find(self, item):
        curNode = self.head
        curItem = curNode.item
        pos = 0
        if curItem == item:
            return curNode
        else:
            pos += 1
            while curItem != item:
                pos += 1
                curNode = curNode.next
                if not curNode:
                    break
                curItem = curNode.item
        return curNode

    # 清空链表
    def clear(self):
        self.length = 0
        self.head = None
        self.last = None

    # 查看链表值
    def view(self):
        items = []
        curNode = self.head
        while curNode:
            items.append(curNode.item)
            curNode = curNode.next
        return items


if __name__ == '__main__':
    link = SLinkList()
    print(link.isEmpty())
    link.add(1)
    link.add(2)
    print(link.isEmpty())
    print(link)
    link.append(5)
    link.append(9)
    print(link)
    link.insert(0, 6)
    link.insert(3, 7)
    print(link)
    link.insert(11, 7)
    print(link)
    link.insert(1, 8)
    print(link)
    print(link[1:3])
    print(link[1])
    print(len(link))
    link.remove(6)
    print(link)
    from collections import Iterable, Iterator
    print(isinstance(link, Iterable))
    print(link.find(2).next)
    link.remove(5)
    link.remove(5)
    link.remove(2)
    link.remove(7)
    print(link)
    print('last=', link.last)
    # for i, x in enumerate(link):
    #     print(i, x)
