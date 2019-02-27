#!/usr/bin/env python
# encoding: utf-8


class Node(object):
    def __init__(self, item):
        self.item = item
        self.next = None


class Stack(object):
    def __init__(self):
        '''
        :param head: 头部，进出端
        :param tail: 尾部，进入的第一个元素
        :param length: 长度
        :return:
        '''
        self.head = None
        self.tail = None
        self.length = 0

    def __repr__(self):
        stack = []
        if not self.isEmpty():
            curNode = self.head
            while curNode:
                stack.append(curNode.item)
                curNode = curNode.next
        return repr(stack)

    def __len__(self):
        return self.length

    def put(self, item):
        newNode = Node(item)
        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head = newNode
        self.length += 1

    def pop(self):
        if self.isEmpty():
            raise IndexError("Stack is empty!")
        item = self.head.item
        self.head = self.head.next
        self.length -= 1
        if self.isEmpty():
            self.tail = None
        return item

    def clear(self):
        self.head = None
        self.tail = None

    def top(self):
        return self.head

    def isEmpty(self):
        return bool(self.head is None)


if __name__ == '__main__':
    s = Stack()
    print(s.isEmpty())
    s.put(1)
    s.put(2)
    s.put(3)
    s.put(4)
    print(s)
    print('len=', len(s))
    print('head=', s.head.item)
    print('tail=', s.tail.item)
    print(s.pop())
    print(s)
    print('len=', len(s))
    print('head=', s.head.item)
    print('tail=', s.tail.item)
    print(s.pop())
    print(s)
    print('len=', len(s))
    print('head=', s.head.item)
    print('tail=', s.tail.item)
    s.put(4)
    print(s)
    print('len=', len(s))
    print('head=', s.head.item)
    print('tail=', s.tail.item)

    print(s.isEmpty())
    # print(s.pop())
