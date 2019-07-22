#!/usr/bin/env python
# encoding: utf-8

'''

@author: senlian

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@file: UpdateServer.py

@time: 2018/9/18 17:11

@module:python -m pip install

@desc: 分布式进程任务，实现内网资源更新
1、服务端监听连接
2、客户端连接服务端并发送任务
3、服务端处理接受到的任务
4、客户端上传包
'''
import os, shutil
import win32file, zipfile, json
import socketserver, hmac
from multiprocessing import freeze_support, Process
# 需要更改
BindIPs = []
StopIPs = []
AuthKey = '123456'
SrcDir = r'D:\WR-GameServer\py\gameserver_update\gmserver'

class SocketServerHandler(socketserver.BaseRequestHandler):
    def setup(self):
        print(self.client_address)
        status = '0'.encode('utf-8')
        urandom = os.urandom(32)
        # 发送加密方式
        self.request.send(urandom)
        self.GetKey = self.request.recv(1024).decode('utf-8')

        if BindIPs and self.client_address[0] not in BindIPs:
            status = '10001'.encode('utf-8')
        elif StopIPs and self.client_address[0] in StopIPs:
            status = '10002'.encode('utf-8')
        else:
            self.AuthKey = hmac.new(AuthKey.encode('utf-8'), urandom).hexdigest()
            if self.GetKey == self.AuthKey:
                self.request.sendall(status)
                return True
            else:
                status = '10003'.encode('utf-8')
        self.request.sendall(status)
        self.request.close()
        return False

    def handle(self):
        if not self.request:
            return False
        while True:
            try:
                self.job, self.SrcIP, self.SrcID, self.SrcType = self.request.recv(1024).decode('utf-8').split(',')
                if (self.job and self.SrcIP and self.SrcID and self.SrcType):
                    if self.job == 'Upload':
                        self.DownLoad()
                    else:
                        self.request.sendall("Error0".encode('utf-8'))
                else:
                    self.request.sendall("Error0".encode('utf-8'))
                    continue
            except Exception as e:
                print(e, self.client_address)
                self.request.close()
                break

    # TODO: 资源下载
    def DownLoad(self):
        print(self.job)
        self.request.sendall("GetFileInfo".encode('utf-8'))
        FileName, FileSize = self.request.recv(1024).decode('utf-8').split(',')
        import time
        FilePath = os.path.join(SrcDir, time.strftime("%Y%m%d"), FileName)
        if FileName and FileSize:
            try:
                if not os.path.isdir(os.path.dirname(FilePath)):
                    os.makedirs(os.path.dirname(FilePath))
                if os.path.isfile(FilePath):
                    shutil.rmtree(FilePath)
                self.request.sendall("Upload".encode('utf-8'))
            except Exception as e:
                print(e)
                self.request.sendall("OtherUsed".encode('utf-8'))
                return False

            try:
                f = open(FilePath, 'wb')
                RecvSize = 0
                while RecvSize < int(FileSize):
                    data = self.request.recv(1024)
                    RecvSize += len(data)
                    f.write(data)
                    print(RecvSize)
                f.close()
                print('download over')
            except:
                self.request.sendall("Error2".encode('utf-8'))
                return False
            finally:
                f.close()
        else:
            self.request.sendall("Error3".encode('utf-8'))
            return False
        return True


if __name__ == '__main__':
    freeze_support()
    # 需要更改
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 8000), SocketServerHandler)
    server.serve_forever()

