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
import time
import os, sys, hmac, re
import wx, wx.aui, wx.adv
import wx.stc as STC
import socket, threading
from multiprocessing import freeze_support
from common.ComponentID import *

print(wx.version())
VERSION = time.strftime("%Y.%m.%d")

wildcard = u"zip files (*.zip)|*.zip|" \
           "rar files (*.rar)|*.rar|" \
           "tar files (*.tar)|*.tar|" \
           "txt files (*.txt)|*.txt|" \
           "csv files (*.csv)|*.csv|" \
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
        self.SetTitle(u'客户端更新工具--v.{0}'.format(VERSION))
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
        self.ctrl = wx.adv.AnimationCtrl(self, wx.NewIdRef(), pos=(0,0),size=(460,150))
        gif_name = r'E:\GitHub\py3\socketDemo1\2.gif'
        gif = self.ctrl.LoadFile(gif_name, wx.adv.ANIMATION_TYPE_GIF)

        self.ctrl.SetBackgroundColour(self.GetBackgroundColour())
        self.ctrl.Play()
        self.OnInit()

    def OnInit(self):
        self.FT_9RNB = wx.Font(9, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.FT_29RNB = wx.Font(29, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.vBox = wx.BoxSizer(wx.VERTICAL)

        self.BtnSwitch = wx.Button(self, id=ID_C_BtnSwitch, label=">", size=(15, 15))
        self.BtnSwitch.SetForegroundColour(wx.BLUE)

        self.BtnUpdate = wx.Button(self, ID_C_BtnUpdate, "更    新")
        self.BtnUpdate.SetFont(self.FT_29RNB)
        self.BtnUpdate.SetForegroundColour(wx.BLUE)

        self.vBox.Add(self.BtnSwitch, 0, wx.LEFT | wx.EXPAND, 435)
        # self.vBox.Add(self.ctrl)
        self.vBox.Add(self.ServerFace())
        self.vBox.AddSpacer(15)
        self.vBox.Add(self.ClientFace())
        self.vBox.AddSpacer(10)
        self.vBox.Add(self.BtnUpdate, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.vBox)

    def ServerFace(self):
        _stBox = wx.StaticBox(parent=self, id=wx.NewIdRef(), label="资源服配置")
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

        _btnConnet = wx.Button(self, ID_C_BtnCnt, "启动连接")

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
        _stBox = wx.StaticBox(parent=self, id=wx.NewIdRef(), label="更新设置")
        _stBoxS = wx.StaticBoxSizer(_stBox, wx.VERTICAL)
        _hBox1 = wx.BoxSizer(wx.HORIZONTAL)

        # _stTextIP = wx.StaticText(self, -1, '服务器:')
        # _stTextIP.SetFont(self.FT_9RNB)
        # _TextIP = wx.TextCtrl(self, ID_C_IP, '192.168.1.13')
        # _TextIP.Bind(wx.EVT_KILL_FOCUS, self.CheckIP)
        #
        # _stTextGameID = wx.StaticText(self, -1, '游戏代号:')
        # _stTextGameID.SetFont(self.FT_9RNB)
        # _GameList = ["1000", "1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010", "1011",
        #              "1012", "1013", "1014", "1015", "1016", "1017", "1018", "1019", "1020", "1021", "1022", "1023",
        #              "1024", "1025", "1026"]
        # _TextGameID = wx.ComboBox(parent=self, id=ID_C_PkgID, value="1000", choices=_GameList)
        # _TextGameID.Bind(wx.EVT_KILL_FOCUS, self.CheckNumber)
        #
        # _stTextGameType = wx.StaticText(self, -1, '客户端类型:')
        # _stTextGameType.SetFont(self.FT_9RNB)
        # _TextGameType = wx.ComboBox(parent=self, id=ID_C_PkgType, value="热更新包", choices=["热更新包", "整包"],
        #                             style=wx.CB_READONLY)

        # _hBox1.Add(_stTextIP, 1, wx.LEFT | wx.EXPAND, 5)
        # _hBox1.Add(_TextIP)

        # _hBox1.Add(_stTextGameID, 1, wx.LEFT | wx.EXPAND, 10)
        # _hBox1.Add(_TextGameID)

        # _hBox1.Add(_stTextGameType, 1, wx.LEFT | wx.EXPAND, 10)
        # _hBox1.Add(_TextGameType)
        # _hBox1.AddSpacer(5)

        _hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        _CkBox1 = wx.StaticText(self, -1, '设备选择：')
        _CkBox1.SetFont(self.FT_9RNB)
        _CkBox2 = wx.CheckBox(self, ID_C_Windows, '平台', style=wx.CHK_2STATE)
        _CkBox3 = wx.CheckBox(self, ID_C_MAC, '游戏')
        _CkBox4 = wx.CheckBox(self, ID_C_Android, 'Web')
        # _CkBox5 = wx.CheckBox(self, ID_Ios, 'ios')
        # _DeviceDir = wx.StaticText(self, -1, '设备目录：')
        # _TextDevice = wx.TextCtrl(self, ID_C_SubDir, '1')
        # _TextDevice.Bind(wx.EVT_KILL_FOCUS, self.CheckNumber)
        # _DeviceDir.SetFont(self.FT_9RNB)
        _CkBox2.SetValue(True)
        _CkBox3.SetValue(True)
        _CkBox4.SetValue(True)
        # _CkBox5.SetValue(True)

        _hBox2.AddSpacer(5)
        _hBox2.Add(_CkBox1)
        _hBox2.Add(_CkBox2)
        _hBox2.AddSpacer(5)
        _hBox2.Add(_CkBox3)
        _hBox2.AddSpacer(5)
        _hBox2.Add(_CkBox4)
        _hBox2.AddSpacer(5)
        # _hBox2.Add(_CkBox5)
        # _hBox2.AddSpacer(10)
        # _hBox2.Add(_DeviceDir)
        # _hBox2.Add(_TextDevice, 1, wx.RIGHT | wx.EXPAND, 5)

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

    def GetSrcFile(self):
        return str(self.FindWindowById(ID_C_SrcFile).GetValue())

    def GetUpdateInfo(self):
        _SrcIP = str(self.FindWindowById(ID_C_IP).GetValue())
        _SrcID = int(self.FindWindowById(ID_C_PkgID).GetValue())
        _SrcType = str(self.FindWindowById(ID_C_PkgType).GetValue())
        return _SrcIP, _SrcID, _SrcType

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

    def GetParameter(self):
        DeviceIds = [ID_C_Windows, ID_C_MAC, ID_C_Android, ID_Ios]
        parameters = []
        for id in DeviceIds:
            item = self.FindWindowById(id)
            if item.GetValue():
                parameters.append(item.GetLabel())
        subdirItem = self.FindWindowById(ID_C_SubDir)
        parameters.append(subdirItem.GetValue())
        return parameters


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
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnOpenFile, id=ID_C_BtnOpenFile)
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnSrc, id=ID_C_BtnSrc)
        self.Bind(wx.EVT_BUTTON, self.OnClickUpdate, id=ID_C_BtnUpdate)

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
        if BtnConnect.GetLabel() == '断开连接':
            if self.ServerPipe:
                self.ServerPipe.close()
                self.right.AppendWarn('断开资源服连接,%s:%s!' % (self.ServerIP, self.ServerPort))

            self.GetParent().GetStatusBar().SetStatusText('', 1)
            self.GetParent().GetStatusBar().SetStatusText('', 2)

            BtnConnect.SetLabel('启动连接')
            BtnConnect.SetForegroundColour(wx.BLACK)
            BtnConnect.Update()
            if e:
                e.Skip()
            return True

        BtnConnect.SetLabel('连接中..')
        BtnConnect.SetForegroundColour(wx.BLUE)
        BtnConnect.Update()

        self.ServerIP, self.ServerPort, self.ServerKey = self.left.GetServerInfo()
        try:
            self.ServerPipe = SocketClient()
            self.ServerPipe.client(self.ServerIP, self.ServerPort, self.ServerKey)
            BtnConnect.SetLabel('断开连接')
            BtnConnect.SetForegroundColour(wx.RED)
            print(self.ServerPipe.getsockname())
            self.GetParent().GetStatusBar().SetStatusText(':'.join(map(str, self.ServerPipe.getsockname())), 1)
            self.GetParent().GetStatusBar().SetStatusText('连接成功', 2)
            self.right.AppendInfo('连接资源服务器成功,%s:%s' % (self.ServerIP, self.ServerPort))
            self.right.AppendInfo(':'.join(map(str, self.ServerPipe.getsockname())))
            self.dialog.info('ok')
        except Exception as error:
            time.sleep(0.5)
            BtnConnect.SetLabel('启动连接')
            BtnConnect.SetForegroundColour(wx.BLACK)

            self.right.AppendError(error.__str__())
            self.right.AppendInfo('连接资源服务器失败,%s:%s' % (self.ServerIP, self.ServerPort))
            self.dialog.warn(error.__str__())
        finally:
            BtnConnect.Update()
            if e:
                e.Skip()
        return True

    def OnClickBtnOpenFile(self, e):
        SrcFile = OpenFileDialog(self)
        self.FindWindowById(ID_C_SrcFile).SetValue(SrcFile)
        return e.Skip()

    def OnClickBtnSrc(self, e):
        SrcFile = self.left.GetSrcFile()
        if not os.path.isfile(SrcFile):
            self.dialog.warn('资源文件路径为空或资源不存在!')
            return e.Skip()
        FileSize = os.stat(SrcFile).st_size
        self.SrcIP, self.SrcID, self.SrcType = self.left.GetUpdateInfo()
        self.right.AppendInfo("准备上传资源，服务器IP: %s，游戏ID: %s,资源类型: %s。" % (self.SrcIP, self.SrcID, self.SrcType))
        try:
            self.ServerPipe.sendall(("Upload,%s,%s,%s" % (self.SrcIP, self.SrcID, self.SrcType)).encode('utf-8'))
            ask = self.ServerPipe.recv(1024).decode('utf-8')
            if ask == 'GetFileInfo':
                self.ServerPipe.sendall(("%s,%s" % (os.path.basename(SrcFile), FileSize)).encode('utf-8'))
                ask2 = self.ServerPipe.recv(1024).decode('utf-8')
                if ask2 == 'Upload':
                    UpSize = 0
                    fopen = open(SrcFile, 'rb')
                    while UpSize < FileSize:
                        if FileSize - UpSize <= 1024:
                            data = fopen.read(FileSize - UpSize)
                            UpSize = FileSize
                        else:
                            data = fopen.read(1024)
                            UpSize += 1024
                        self.ServerPipe.sendall(data)
                        print(UpSize)
                    fopen.close()
                    self.right.AppendInfo("上传成功。")
                    self.dialog.info("上传成功。")
                elif ask2 == 'OtherUsed':
                    self.right.AppendWarn("%s,有其他大佬，也在上传该资源!" % ask2)
                    self.dialog.warn("有其他大佬，也在上传该资源!")
                else:
                    self.right.AppendWarn("%s,未知原因导致资源上传失败!" % ask2)
                    raise ExceptionMsg("未知原因导致资源上传失败!")
            elif ask == 'Error1':
                self.right.AppendWarn("%s, 服务器未部署'%s'的资源网站,请联系苦逼运维!" % (ask, self.SrcIP))
                self.dialog.warn("服务器未部署'%s'的资源网站,请联系苦逼运维!" % self.SrcIP)
            else:
                self.right.AppendWarn("%s,未知原因导致资源上传失败!" % (ask, self.SrcIP))
                raise ExceptionMsg("未知原因导致资源上传失败!")
        except Exception as error:
            self.dialog.error(error.__str__())
            self.right.AppendError(error.__str__())
            self.right.AppendWarn("上传资源失败!")
            BtnConnect = self.FindWindowById(ID_C_BtnCnt)
            BtnConnect.SetLabel('启动连接')
            BtnConnect.SetForegroundColour(wx.BLACK)
        finally:
            e.Skip()

    def OnClickUpdate(self, e):
        self.SrcIP, self.SrcID, self.SrcType = self.left.GetUpdateInfo()
        self.right.AppendInfo("准备更新资源，服务器IP: %s，游戏ID: %s,资源类型: %s。" % (self.SrcIP, self.SrcID, self.SrcType))
        try:
            self.ServerPipe.sendall(("Update,%s,%s,%s" % (self.SrcIP, self.SrcID, self.SrcType)).encode('utf-8'))
            ask_pre = self.ServerPipe.recv(1024).decode('utf-8')
            if ask_pre == 'Update':
                self.ServerPipe.sendall((",".join(self.left.GetParameter())).encode('utf-8'))
            else:
                self.right.AppendWarn("%s, 服务器未部署'%s'的资源网站,请联系苦逼运维!" % (ask_pre, self.SrcIP))
                self.dialog.warn("服务器未部署'%s'的资源网站,请联系苦逼运维!" % self.SrcIP)
                return e.Skip()

            ask = self.ServerPipe.recv(1024).decode('utf-8')
            self.ServerPipe.settimeout(10)
            if ask == 'Error1':
                self.right.AppendWarn("%s, 服务器未部署'%s'的资源网站,请联系苦逼运维!" % (ask, self.SrcIP))
                self.dialog.warn("服务器未部署'%s'的资源网站,请联系苦逼运维!" % self.SrcIP)
            elif ask == 'Error4':
                self.right.AppendError("%s, 资源未上传或资源丢失!" % ask)
                self.dialog.error("资源未上传或资源丢失!")
            elif ask == 'Error5':
                self.right.AppendWarn("%s, 平台没有整包!" % ask)
                self.dialog.warn("别逗，平台没有整包!")
            elif ask == 'ok':
                self.right.AppendWarn("更新成功!")
                self.dialog.info("更新成功!")
            else:
                self.right.AppendError(ask)
                self.right.AppendError("未知原因导致更新失败,请联系苦逼运维!")
                self.dialog.error("%s\r\n未知原因导致更新失败,请联系苦逼运维!" % ask)
        except Exception as error:
            self.dialog.error(error.__str__())
            self.right.AppendError(error.__str__())
            self.right.AppendWarn("更新资源失败!")
            BtnConnect = self.FindWindowById(ID_C_BtnCnt)
            BtnConnect.SetLabel('启动连接')
            BtnConnect.SetForegroundColour(wx.BLACK)
        finally:
            e.Skip()


class SocketClient(socket.socket):
    def __init__(self, host="192.168.1.148", port=5000, authkey=b"123456"):
        super(SocketClient, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.settimeout(5)

    def client(self, host, port, authkey=''):
        try:
            self.connect((host, port))
        except Exception as e:
            raise e
        # 获取加密方式
        urandom = self.recv(1024)

        # 发送密钥
        authkey = hmac.new(authkey.encode('utf-8'), urandom).hexdigest().encode('utf-8')
        self.sendall(authkey)

        # 接收连接状态
        status = self.recv(1024).decode('utf-8')

        if status == '0':
            return True
        elif status == '10001':
            self.shutdown(socket.SHUT_RDWR)
            self.close()
            raise ExceptionMsg('[Connect Error 10001] 服务端拒绝该IP访问,连接不通过。')
        elif status == '10002':
            self.shutdown(socket.SHUT_RDWR)
            self.close()
            raise ExceptionMsg('[Connect Error 10002] 服务端拒绝该IP访问,连接不通过。')
        elif status == '10003':
            self.shutdown(socket.SHUT_RDWR)
            self.close()
            raise ExceptionMsg('[Connect Error 10003] 密码验证失败,连接不通过。')
        else:
            self.shutdown(socket.SHUT_RDWR)
            self.close()
            raise ExceptionMsg('[Connect Error] 未知原因,无法连接。')


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
