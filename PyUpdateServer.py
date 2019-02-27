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

import os, sys, shutil
import win32file, zipfile, json
import socketserver, hmac, socket
import win32event, winerror, win32serviceutil, win32service, servicemanager
from multiprocessing import freeze_support, Process


class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PythonService'
    _svc_display_name_ = 'PythonService'
    _svc_description_ = 'PythonService'

    def __init__(self, args=None):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True
        socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        try:
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.main()
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED,
                                  (self._svc_name_, ''))
        except Exception as e:
            servicemanager.LogErrorMsg(e.__str__())
            self.SvcStop()

    def SvcStop(self):
        try:
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            self.isAlive = False
            win32event.SetEvent(self.hWaitStop)
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        except Exception as e:
            servicemanager.LogErrorMsg(e.__str__())
        finally:
            self.isAlive = False

    def main(self):
        while self.isAlive:
            signal = win32event.WaitForSingleObject(self.hWaitStop, 24 * 60 * 60)
            if signal == win32event.WAIT_OBJECT_0:
                servicemanager.LogWarningMsg(self._svc_name_ + 'Stoped !')
                break
            try:
                servicemanager.LogInfoMsg(self._svc_name_ + 'Starting Job!')
                import threading
                threading.Thread(target=self.DoJob)
                servicemanager.LogInfoMsg(self._svc_name_ + 'Finish Job!')
            except Exception as e:
                servicemanager.LogErrorMsg(e.__str__())
                self.SvcStop()

    def DoJob(self):
        pass


if __name__ == '__main__':
    # from PyInstaller.__main__ import run
    freeze_support()
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(PythonService)
            servicemanager.Initialize(PythonService.__name__, evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details.args[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(PythonService)
