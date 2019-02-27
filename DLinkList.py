#!/usr/bin/env python
# encoding: utf-8

# TODO: 定义双向链表节点
class Node(object):
    def __init__(self, item=None):
        '''
        :param item: 记录当前节点值
        :param prev: 记录前一个节点
        :param next: 记录下一个节点
        :return: None
        '''
        self.item = item
        self.prev = None
        self.next = None

    def __repr__(self):
        return repr(self.item)


# TODO: 定义双向链表
class DLinkList(object):
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
        '''
        repr类似给原有对象加引号；
        str则是将原对象转换成字符串格式。
        '''
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
        # index为<class 'slice'>或者<class 'int'>类型
        # print(type(index))
        try:
            return self.view()[index]
        except IndexError as e:
            raise e

    # 标示可迭代
    def __iter__(self):
        return self

    # 适用next方法，实现可迭代
    def __next__(self):
        # StopIteration抛出越界异常，否则死循环
        if not self.head or self.index >= self.length:
            raise StopIteration
        else:
            if not self.curNode:
                self.curNode = self.head
            curItem = self.curNode.item
            self.curNode = self.curNode.next
            self.index += 1
        return curItem

    # 判断链表是否为空
    def isEmpty(self):
        return self.head is None

    # 头部添加节点
    def add(self, item):
        newNode = Node(item)
        newNode.prev = None
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
        newNode.prev = self.last
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
            while count < pos:
                count += 1
                preNode = curNode
                curNode = curNode.next

            preNode.next = newNode
            newNode.prev = preNode
            newNode.next = curNode
            curNode.prev = newNode

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
                if self.head:
                    self.head.prev = None
            else:
                while item != curItem:
                    preNode = curNode or None
                    curNode = curNode.next or None
                    nextNode = None if not curNode else curNode.next
                    curItem = None if not curNode else curNode.item
                preNode.next = nextNode
                if nextNode:
                    nextNode.prev = preNode
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
    from collections import Iterable

    link = DLinkList()
    print(link.isEmpty())
    link.append(1)
    link.add(2)
    link.add(3)
    print(link)
    link.append(4)
    print(link)
    link.insert(0, 'a')
    link.insert(2, 'b')
    print(link)
    link.insert(9, 'c')
    print(link.isEmpty())
    link.remove(3)
    link.remove(4)
    link.remove('2')
    print(link)
    print(link[2])
    print(link[1:3])
    print('last=', link.last)
