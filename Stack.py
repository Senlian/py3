#!/usr/bin/env python
# encoding: utf-8

# TODO: 栈, 一端操作，后进先出，先进后出
class Stack(object):
    def __init__(self):
        self.stack = []

    def __repr__(self):
        return repr(self.stack)

    def __len__(self):
        return len(self.stack)

    def put(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def clear(self):
        self.stack = []

    def top(self):
        return self.stack[-1]

    def isEmpty(self):
        return bool(self.stack)


if __name__ == '__main__':
    s = Stack()
    print(s.isEmpty())
    s.put(0)
    s.put(1)
    s.put(2)
    print(s)
    print(len(s))
    s.pop()
    print(s)
    s.pop()
    print(s)
    print(s.isEmpty())
