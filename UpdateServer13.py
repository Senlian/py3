#!/usr/bin/env python
# encoding: utf-8

'''

@author: senlian

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@file: UpdateClient.py

@time: 2018/9/18 17:16

@module:python -m pip install

@desc:
python 3.6.3
'''
import wx, wx.aui
import wx.stc as STC
import time, os, sys, shutil
import win32file, zipfile, json, re
import socket, socketserver, hmac
import threading
from multiprocessing import freeze_support, Process
from common.ComponentID import *

BindIPs = []
StopIPs = []
AuthKey = '123456'
SrcDir = r'D:\IIS-Site\ClientResource\ClientPackage\zip'
UnzipDir = r'D:\IIS-Site\ClientResource\ClientPackage\unzip'
BakDir = r'D:\IIS-Site\ClientResource\ClientPackage\bak'
DstDir = r"D:\IIS-Site\ClientResource\{host_id}\hotupdate\GameData"
device_types = ("android", "ios", "mac", "windows")
VERSION = time.strftime("%Y.%m.%d")

wildcard = u"zip files (*.zip)|*.zip|" \
           "rar files (*.rar)|*.rar|" \
           "tar files (*.tar)|*.tar|" \
           "txt files (*.txt)|*.txt|" \
           "tar.gz files (*.tar.gz)|*.tar.gz|" \
           "All files (*.*)|*.*"


# TODO: 打开文件


def OpenFileDialog(parent=None, defaultDir='', defaultFile=''):
    if not defaultDir:
        defaultDir = defaultFile
    if not parent:
        return False

    dlg = wx.FileDialog(parent, message=u"打开",
                        defaultDir=defaultDir,
                        defaultFile=defaultFile,
                        wildcard=wildcard,
                        style=wx.FD_OPEN)
    targetFile = defaultFile
    if dlg.ShowModal() == wx.ID_OK:
        targetFile = dlg.GetPath()
    dlg.Destroy()
    return targetFile


# TODO: 主体框架
class RootFrame(wx.Frame):
    def __init__(self, parent=None):
        super(RootFrame, self).__init__(parent=parent, id=ID_C_Root)
        self.settings()

    def settings(self):
        self.SetTitle(u'客户端更新工具--s.v.{0}'.format(VERSION))
        self.SetSize((460, 400))
        self.SetMinClientSize((460, 400))
        self.SetMaxClientSize((920, 400))
        self.SetTransparent(230)
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        # self.SetIcon(PyEmbeddedImage(B64_POKER128).GetIcon())
        self.Center()
        self.TaskBarIcon = None
        self.InitUI()

    def InitUI(self):
        HomePage(self)
        StatusBar(self)


class Dialogs(wx.MessageDialog):
    def __init__(self, parent=None):
        self.parent = parent

    def info(self, msg):
        style = wx.ICON_INFORMATION
        super(Dialogs, self).__init__(parent=self.parent, caption="提示", message=msg, style=style)
        self.ShowModal()

    def warn(self, msg):
        style = wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION
        super(Dialogs, self).__init__(parent=self.parent, caption="警告", message=msg, style=style)
        self.ShowModal()

    def error(self, msg):
        style = wx.OK | wx.CANCEL | wx.ICON_ERROR
        super(Dialogs, self).__init__(parent=self.parent, caption="错误", message=msg, style=style)
        self.ShowModal()


# TODO: 状态栏
class StatusBar(wx.StatusBar):
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent=parent, id=-1, style=65840, name=u'状态栏')
        self.SetFieldsCount(3)
        self.SetStatusWidths([-2, -2, -1])
        self.Show()
        if parent:
            parent.SetStatusBar(self)


# TODO: 设置界面
class LeftPage(wx.Panel):
    def __init__(self, parent=None):
        super(LeftPage, self).__init__(parent=parent)
        self.dialog = Dialogs(self)
        self.OnInit()

    def OnInit(self):
        self.FT_9RNB = wx.Font(9, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.FT_29RNB = wx.Font(29, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.vBox = wx.BoxSizer(wx.VERTICAL)

        self.BtnSwitch = wx.Button(self, id=ID_C_BtnSwitch, label=">", size=(15, 15))
        self.BtnSwitch.SetForegroundColour(wx.BLUE)

        self.vBox.Add(self.BtnSwitch, 0, wx.LEFT | wx.EXPAND, 435)
        self.vBox.Add(self.ServerFace())
        self.vBox.AddSpacer(10)

        self.SetSizer(self.vBox)

    def ServerFace(self):
        _stBox = wx.StaticBox(parent=self, id=wx.NewId(), label="资源服配置")
        _stBoxS = wx.StaticBoxSizer(_stBox, wx.VERTICAL)
        _hBox = wx.BoxSizer(wx.HORIZONTAL)

        _stTextIP = wx.StaticText(self, -1, 'IP:')
        _stTextIP.SetFont(self.FT_9RNB)
        _TextIP = wx.TextCtrl(self, ID_C_SIP, '192.168.1.18')
        _TextIP.Bind(wx.EVT_KILL_FOCUS, self.CheckIP)
        _stTextPort = wx.StaticText(self, -1, '端口号:')
        _stTextPort.SetFont(self.FT_9RNB)
        _TextPort = wx.TextCtrl(self, ID_C_SPort, '5000', size=(40, self.GetSize()[1]))
        _TextPort.Bind(wx.EVT_KILL_FOCUS, self.CheckNumber)

        _stTextKey = wx.StaticText(self, -1, '口令:')
        _stTextKey.SetFont(self.FT_9RNB)
        _TextKey = wx.TextCtrl(self, ID_C_SKey, '123456')

        _btnConnet = wx.Button(self, ID_C_BtnCnt, "启动服务")

        _hBox.Add(_stTextIP, 1, wx.LEFT | wx.EXPAND, 5)
        _hBox.Add(_TextIP)

        _hBox.Add(_stTextPort, 1, wx.LEFT | wx.EXPAND, 10)
        _hBox.Add(_TextPort)

        _hBox.Add(_stTextKey, 1, wx.LEFT | wx.EXPAND, 10)
        _hBox.Add(_TextKey)

        _hBox.Add(_btnConnet, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)

        _stBoxS.Add(_hBox, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)

        return _stBoxS

    def ClientFace(self):
        _stBox = wx.StaticBox(parent=self, id=wx.NewId(), label="更新设置")
        _stBoxS = wx.StaticBoxSizer(_stBox, wx.VERTICAL)
        _hBox1 = wx.BoxSizer(wx.HORIZONTAL)

        _stTextIP = wx.StaticText(self, -1, '服务器:')
        _stTextIP.SetFont(self.FT_9RNB)
        _TextIP = wx.TextCtrl(self, ID_C_IP, '192.168.1.13')
        _TextIP.Bind(wx.EVT_KILL_FOCUS, self.CheckIP)

        _stTextGameID = wx.StaticText(self, -1, '游戏代号:')
        _stTextGameID.SetFont(self.FT_9RNB)
        _GameList = ["1000", "1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010", "1011",
                     "1012", "1013", "1014", "1015", "1016", "1017", "1018", "1019", "1020", "1021", "1022", "1023",
                     "1024", "1025", "1026"]
        _TextGameID = wx.ComboBox(parent=self, id=ID_C_PkgID, value="1000", choices=_GameList)
        _TextGameID.Bind(wx.EVT_KILL_FOCUS, self.CheckNumber)

        _stTextGameType = wx.StaticText(self, -1, '客户端类型:')
        _stTextGameType.SetFont(self.FT_9RNB)
        _TextGameType = wx.ComboBox(parent=self, id=ID_C_PkgType, value="热更新包", choices=["热更新包", "整包"],
                                    style=wx.CB_READONLY)

        _hBox1.Add(_stTextIP, 1, wx.LEFT | wx.EXPAND, 5)
        _hBox1.Add(_TextIP)

        _hBox1.Add(_stTextGameID, 1, wx.LEFT | wx.EXPAND, 10)
        _hBox1.Add(_TextGameID)

        _hBox1.Add(_stTextGameType, 1, wx.LEFT | wx.EXPAND, 10)
        _hBox1.Add(_TextGameType)
        _hBox1.AddSpacer(5)

        _hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        _CkBox1 = wx.StaticText(self, -1, '设备选择：')
        _CkBox1.SetFont(self.FT_9RNB)
        _CkBox2 = wx.CheckBox(self, ID_C_Windows, 'windows', style=wx.CHK_2STATE)
        _CkBox3 = wx.CheckBox(self, ID_C_MAC, 'mac')
        _CkBox4 = wx.CheckBox(self, ID_C_Android, 'android')
        _CkBox5 = wx.CheckBox(self, ID_Ios, 'ios')
        _DeviceDir = wx.StaticText(self, -1, '设备目录：')
        _TextDevice = wx.TextCtrl(self, ID_C_SubDir, '1')
        _TextDevice.Bind(wx.EVT_KILL_FOCUS, self.CheckNumber)
        _DeviceDir.SetFont(self.FT_9RNB)
        _CkBox2.SetValue(True)
        _CkBox3.SetValue(True)
        _CkBox4.SetValue(True)
        _CkBox5.SetValue(True)

        _hBox2.AddSpacer(5)
        _hBox2.Add(_CkBox1)
        _hBox2.Add(_CkBox2)
        _hBox2.AddSpacer(5)
        _hBox2.Add(_CkBox3)
        _hBox2.AddSpacer(5)
        _hBox2.Add(_CkBox4)
        _hBox2.AddSpacer(5)
        _hBox2.Add(_CkBox5)
        _hBox2.AddSpacer(10)
        _hBox2.Add(_DeviceDir)
        _hBox2.Add(_TextDevice, 1, wx.RIGHT | wx.EXPAND, 5)

        _hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        _TextSrc = wx.TextCtrl(self, ID_C_SrcFile, "")
        _btnFindSrc = wx.Button(self, ID_C_BtnOpenFile, "浏览...")
        _btnSrc = wx.Button(self, ID_C_BtnSrc, "资源上传")
        _hBox3.Add(_TextSrc, 1, wx.LEFT | wx.EXPAND, 5)
        _hBox3.Add(_btnFindSrc)
        _hBox3.AddSpacer(5)
        _hBox3.Add(_btnSrc)
        _hBox3.AddSpacer(5)

        _stBoxS.Add(_hBox1, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        _stBoxS.Add(_hBox2, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        _stBoxS.Add(_hBox3, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)

        return _stBoxS

    def GetServerInfo(self):
        _ServerIP = str(self.FindWindowById(ID_C_SIP).GetValue())
        _ServerPort = int(self.FindWindowById(ID_C_SPort).GetValue())
        _ServerKey = str(self.FindWindowById(ID_C_SKey).GetValue())
        return _ServerIP, _ServerPort, _ServerKey

    def CheckIP(self, e):
        curId = e.GetId()
        item = self.FindWindowById(curId)
        value = item.GetValue()
        ip_pattern = '^((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$'
        pattern = re.compile(ip_pattern)
        if not (pattern.match(value)):
            self.dialog.warn("格式错误,请输入正确的IP地址！")
            item.SetValue('192.168.1.18')
            item.SetFocus()
        e.Skip()

    def CheckNumber(self, e):
        curId = e.GetId()
        item = self.FindWindowById(curId)
        value = item.GetValue()
        if not value.isdigit():
            if curId == ID_C_SPort:
                self.dialog.warn("格式错误，端口号为1~65535间的数字！")
                item.SetValue('5000')
            else:
                self.dialog.warn("格式错误，请数入数字！")
                if curId == ID_C_PkgID:
                    item.SetValue('1000')
                else:
                    item.SetValue('1')
            item.SetFocus()
        if curId == ID_C_SPort and (int(value) not in range(1, 65536)):
            self.dialog.warn("格式错误，端口号为1~65535间的数字！")
            item.SetValue('5000')
            item.SetFocus()
        e.Skip()


# TODO: 日志界面
class RightPage(STC.StyledTextCtrl):
    def __init__(self, parent=None):
        self.TextStyle = STC.STC_STYLE_DEFAULT + STC.STC_STYLE_CONTROLCHAR
        super(RightPage, self).__init__(parent=parent, id=ID_C_TeLog, style=self.TextStyle)

        self.SetMarginWidth(1, 16)
        self.SetMarginType(1, STC.STC_MARGIN_NUMBER)

    def ClearText(self, e):
        wx.CallAfter(self.ClearAll)
        if e:
            e.Skip()

    def AppendInfo(self, text):
        text = str(time.strftime("[%y-%m-%d %H:%M:%S INFO]")) + " %s\r\n" % text
        wx.CallAfter(self.AppendText, text=text)
        self.ScrollToEnd()

    def AppendWarn(self, text):
        text = str(time.strftime("[%y-%m-%d %H:%M:%S WARN]")) + " %s\r\n" % text
        wx.CallAfter(self.AppendText, text=text)
        self.ScrollToEnd()

    def AppendError(self, text):
        text = str(time.strftime("[%y-%m-%d %H:%M:%S ERROR]")) + " %s\r\n" % text
        wx.CallAfter(self.AppendText, text=text)
        self.ScrollToEnd()


# TODO: 功能页
class HomePage(wx.SplitterWindow):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent=parent, id=ID_C_HomePage, size=parent.GetSize(),
                                       style=wx.SP_VERTICAL | wx.SP_NOBORDER)
        self.dialog = Dialogs(self)
        self.left = LeftPage(self)
        self.right = RightPage(self)
        self.SetMinimumPaneSize(460)
        self.SplitVertically(self.left, self.right, 460)
        self.ServerPipe = None

        self.Bind(wx.EVT_BUTTON, self.OnClickSwitch, id=ID_C_BtnSwitch)
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnCnt, id=ID_C_BtnCnt)

    def OnClickSwitch(self, e):
        curId = ID_C_BtnSwitch
        if self.FindWindowById(curId).Label == '<':
            self.FindWindowById(curId).SetLabel(">")
            self.GetParent().SetSize((460, 400))
        else:
            self.FindWindowById(curId).SetLabel("<")
            self.GetParent().SetSize((460 * 2, 400))
        e.Skip()

    def OnClickBtnCnt(self, e=None):
        curId = ID_C_BtnCnt
        BtnConnect = self.FindWindowById(curId)
        if BtnConnect.GetLabel() == '关闭服务':
            if self.ServerPipe:
                self.ServerPipe.close()
                self.right.AppendWarn('关闭服务端,%s:%s !' % (self.ServerIP, self.ServerPort))

            self.GetParent().GetStatusBar().SetStatusText('', 1)
            self.GetParent().GetStatusBar().SetStatusText('', 2)

            BtnConnect.SetLabel('启动服务')
            BtnConnect.SetForegroundColour(wx.BLACK)
            BtnConnect.Update()
            if e:
                e.Skip()
            return True

        BtnConnect.SetLabel('启动中..')
        BtnConnect.SetForegroundColour(wx.BLUE)
        BtnConnect.Update()

        self.ServerIP, self.ServerPort, self.ServerKey = self.left.GetServerInfo()
        try:
            self.ServerPipe = SocketTreadServer(self.ServerIP, self.ServerPort, self.ServerKey, self)
            self.ServerPipe.start()
            BtnConnect.SetLabel('关闭服务')
            BtnConnect.SetForegroundColour(wx.RED)
            self.GetParent().GetStatusBar().SetStatusText(self.ServerIP + ':' + str(self.ServerPort), 1)
            self.GetParent().GetStatusBar().SetStatusText('启动成功', 2)
            self.right.AppendInfo('启动服务端成功,%s:%s' % (self.ServerIP, self.ServerPort))
            self.dialog.info('ok')
        except Exception as error:
            time.sleep(0.5)
            BtnConnect.SetLabel('启动服务')
            BtnConnect.SetForegroundColour(wx.BLACK)
            self.right.AppendError(error.__str__())
            self.right.AppendInfo('启动服务端失败,%s:%s' % (self.ServerIP, self.ServerPort))
            self.dialog.warn(error.__str__())
        finally:
            BtnConnect.Update()
            if e:
                e.Skip()
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


class SocketTreadServer(threading.Thread):
    def __init__(self, host="192.168.1.18", port=5000, authkey=b"123456", parent=None):
        super(SocketTreadServer, self).__init__()
        self.server = socketserver.ThreadingTCPServer((host, int(port)), SocketServerHandler)

    def run(self):
        try:
            self.server.serve_forever()
        except Exception as e:
            raise e

    def close(self):
        self.server.shutdown()
        self.server.server_close()



class ExceptionMsg(Exception):
    def __init__(self, msg):
        super(ExceptionMsg, self).__init__(msg)


class NewApp(wx.App):
    def OnInit(self):
        window = RootFrame()
        window.Show()
        return True


if __name__ == '__main__':
    freeze_support()
    app = NewApp()
    app.MainLoop()
