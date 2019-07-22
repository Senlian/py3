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

BindIPs = []
StopIPs = []
AuthKey = '123456'
SrcDir = r'D:\IIS-Site\ClientResource\ClientPackage\zip'
UnzipDir = r'D:\IIS-Site\ClientResource\ClientPackage\unzip'
BakDir = r'D:\IIS-Site\ClientResource\ClientPackage\bak'
DstDir = r"D:\IIS-Site\ClientResource\{host_id}\hotupdate\GameData"
device_types = ("android", "ios", "mac", "windows")


def decompression_folder(zip_file, dst_folder):
    zip_folder = zipfile.ZipFile(zip_file, 'r', allowZip64=True)
    for file in zip_folder.namelist():
        zip_folder.extract(file, dst_folder)


def BackUpDir(src_dir, backup_dir):
    if not os.path.exists(src_dir):
        return False

    if os.path.isdir(backup_dir):
        shutil.rmtree(backup_dir)
    os.makedirs(backup_dir)

    if os.path.isfile(src_dir):
        src_files = [src_dir]
    else:
        src_files = [os.path.join(src_dir, file) for file in os.listdir(src_dir)]

    for src_file in src_files:
        dst_file = os.path.join(backup_dir, os.path.basename(src_file))
        if not os.path.isfile(src_file):
            continue
        win32file.CopyFile(src_file, dst_file, 0)
        print(u"备份'{0}'到'{1}'".format(src_file, dst_file))
    return True


def CopyDir(src_dir, dst_dir, ignore_pattern):
    if not os.path.isdir(src_dir):
        return False

    src_files = [file for file in os.listdir(src_dir) if
                 (os.path.splitext(file) != ignore_pattern and os.path.isfile(os.path.join(src_dir, file)))]
    if len(src_files) == 0:
        return False
    try:
        if os.path.isdir(dst_dir):
            dst_old_files = os.listdir(dst_dir)
            for target in dst_old_files:
                old_file = os.path.join(dst_dir, target)
                if os.path.exists(old_file) and (os.path.splitext(old_file)[1] != ignore_pattern):
                    os.remove(old_file)
        else:
            os.makedirs(dst_dir)

        for file in src_files:
            src_file = os.path.join(src_dir, file)
            dst_file = os.path.join(dst_dir, file)
            if os.path.splitext(src_file)[1] == ignore_pattern:
                continue
            if os.path.isfile(dst_file):
                os.remove(dst_file)
            win32file.CopyFile(src_file, dst_file, 0)
            print(u"更新'{0}'到'{1}'".format(src_file, dst_file))
    except Exception as e:
        print(e)
        return False
    return True


def refresh_iis(url, data):
    from urllib import parse, request
    data = parse.urlencode(data)
    url = url + '?' + data
    print(url)
    rq = request.Request(url)
    response = request.urlopen(rq)
    rtn = response.read()
    try:
        rtn = (rtn.decode("utf-8"))
        rtn = json.loads(rtn)
        if int(rtn['status']) == 1:
            print(rtn['msg'])
            return True
        else:
            print(rtn['msg'])
            return False
    except Exception as e:
        print(rtn)
        return False


def refresh_iis_cache(host_id, game_code, device, subdir):
    root_url = r'http://192.168.1.18:{port}'.format(port=10000 + int(host_id))
    print(u"开始清理缓存...")
    rq_data = {
        "update_type": game_code,
        "platform_type": device,
        "version_code": subdir
    }

    del_data = {
        "update_type": "CLEAR",
        "clearKey": "HotUpdate\{0}\{1}\{2}".format(game_code, device, subdir)
    }

    url = root_url + '/GameDownload.ashx'
    try:
        refresh_iis(url, rq_data)
        return refresh_iis(url, del_data)
    except Exception as e:
        print(e)
        return False


def restart_apppool(pool):
    try:
        _stop = r"C:\Windows\System32\inetsrv\appcmd.exe" + " stop APPPOOL " + pool
        _start = r"C:\Windows\System32\inetsrv\appcmd.exe" + " start  APPPOOL " + pool
        _list = r"C:\Windows\System32\inetsrv\appcmd.exe" + " list  APPPOOL " + pool
        os.popen(_stop)
        while ((os.popen(_list).read().split("state:")[1][:-2].lower()) == "stopped"):
            os.popen(_start)
        print(u"\n重启应用池'{0}'\n".format(pool))
    except Exception as e:
        print(e)
        return False
    return True


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
                if self.SrcType == '热更新包':
                    self.SrcType = 'HotUpdate'
                else:
                    self.SrcType = 'GamePackage'
                self.DstDir = os.path.join(DstDir.format(host_id=self.SrcIP.split('.')[-1]), self.SrcType)
                if (self.job and self.SrcIP and self.SrcID and self.SrcType):
                    if not os.path.isdir(self.DstDir):
                        self.request.sendall("Error1".encode('utf-8'))
                        continue
                    if self.SrcID == '1000':
                        self.SrcID = 'yyplatform'
                    if self.job == 'Upload':
                        self.DownLoad()
                    else:
                        self.Update()
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
        FilePath = os.path.join(SrcDir, self.SrcIP, self.SrcType, self.SrcID, FileName)
        if FileName and FileSize:
            try:
                if os.path.isdir(os.path.dirname(FilePath)):
                    shutil.rmtree(os.path.dirname(FilePath))
                os.makedirs(os.path.dirname(FilePath))
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

    # TODO: 资源更新
    def Update(self):
        self.request.sendall("Update".encode('utf-8'))
        _data = self.request.recv(1024).decode('utf-8').split(',')
        if len(_data) < 2:
            self.request.sendall("Error6".encode('utf-8'))
            return False
        device_types = _data[0:-1] or ("android", "ios", "mac", "windows")
        subDir = _data[-1] or '1'

        print(self.job, self.SrcType, device_types, subDir)
        self.SrcDir = os.path.join(SrcDir, self.SrcIP, self.SrcType, self.SrcID)
        self.DstDir = os.path.join(self.DstDir, self.SrcID)
        self.BakDir = os.path.join(BakDir, self.SrcIP, self.SrcType, self.SrcID)
        if self.SrcType == 'GamePackage':
            if self.SrcID == 'yyplatform':
                self.request.sendall("Error5".encode('utf-8'))
                return False
            BackUpDir(self.DstDir, self.BakDir)
            rst = CopyDir(self.SrcDir, self.DstDir, '.txt')
            if rst:
                self.request.sendall("ok".encode('utf-8'))
                return True
            else:
                self.request.sendall("Error4".encode('utf-8'))
                return False
        else:
            try:
                self.SrcZipFile = os.path.join(self.SrcDir, os.listdir(self.SrcDir)[0])
                self.SrcUnzipDir = os.path.join(UnzipDir, self.SrcIP, self.SrcType, self.SrcID)
                if os.path.isdir(self.SrcUnzipDir):
                    shutil.rmtree(self.SrcUnzipDir)
                decompression_folder(self.SrcZipFile, self.SrcUnzipDir)
                has_bak = False
                for device in device_types:
                    target_dir = os.path.join(self.DstDir, device, subDir)
                    if not has_bak:
                        has_bak = BackUpDir(target_dir, self.BakDir)
                    CopyDir(self.SrcUnzipDir, target_dir, '.txt')
                    rst = CopyDir(self.SrcUnzipDir, target_dir, '.zip')
                    host_id = self.SrcIP.split('.')[-1]
                    if not refresh_iis_cache(host_id, self.SrcID, device, subDir):
                        restart_apppool("HotUpdate_" + host_id)
                    if not rst:
                        self.request.sendall("Error4".encode('utf-8'))
                        return False
                    else:
                        continue
                self.request.sendall("ok".encode('utf-8'))
            except Exception as e:
                self.request.sendall(e.__str__().encode('utf-8'))
                return False
            return True


if __name__ == '__main__':
    freeze_support()
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 5000), SocketServerHandler)
    server.serve_forever()
