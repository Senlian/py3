#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import asyncio
import os, sys, hmac, re
import wx, wx.aui, wx.adv
import wx.stc as STC
import socket, threading
import ftplib
from multiprocessing import freeze_support
from common.ComponentID import *

VERSION = "v2019.07.18.1"

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


class ExceptionMsg(Exception):
    def __init__(self, msg):
        super(ExceptionMsg, self).__init__(msg)


# TODO: 主体框架
class RootFrame(wx.Frame):
    def __init__(self, parent=None):
        super(RootFrame, self).__init__(parent=parent, id=ID_C_Root)
        self.settings()

    def settings(self):
        self.SetTitle(u'FTP上传工具--{0}'.format(VERSION))
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


# TODO: 状态栏
class StatusBar(wx.StatusBar):
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent=parent, id=-1, style=65840, name=u'状态栏')
        self.SetFieldsCount(2)
        self.SetStatusWidths([-2, -1])
        self.Show()
        self.gauge = None
        if parent:
            parent.SetStatusBar(self)

    def CreateGauge(self):
        self.gauge = wx.Gauge(self, wx.NewIdRef(), 100, pos=(5, 3), size=(280, 20), style=wx.GA_HORIZONTAL)
        self.gauge.SetBezelFace(0.5)
        self.gauge.SetShadowWidth(2)
        self.gauge.SetValue(0)

        return self.gauge


class Dialogs(wx.MessageDialog):
    def __init__(self, parent=None):
        self.parent = parent

    def info(self, msg):
        style = wx.ICON_INFORMATION
        super(Dialogs, self).__init__(parent=self.parent, caption="提示", message=msg, style=style)
        return self.ShowModal()

    def warn(self, msg):
        style = wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION
        super(Dialogs, self).__init__(parent=self.parent, caption="警告", message=msg, style=style)
        return self.ShowModal()

    def error(self, msg):
        style = wx.OK | wx.CANCEL | wx.ICON_ERROR
        super(Dialogs, self).__init__(parent=self.parent, caption="错误", message=msg, style=style)
        return self.ShowModal()


class PutPage(wx.Panel):
    def __init__(self, parent=None):
        super(PutPage, self).__init__(parent=parent)
        self.dialog = Dialogs(self)
        self.OnInit()

    def OnInit(self):
        self.FT_9RNB = wx.Font(9, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.FT_29RNB = wx.Font(29, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.vBox = wx.BoxSizer(wx.VERTICAL)

        self.BtnUpdate = wx.Button(self, ID_C_BtnSrc, "上    传")
        self.BtnUpdate.SetFont(self.FT_29RNB)
        self.BtnUpdate.SetForegroundColour(wx.BLUE)

        self.BtnSwitch = wx.Button(self, id=ID_C_BtnSwitch, label=">", size=(15, 15))
        self.BtnSwitch.SetForegroundColour(wx.BLUE)
        self.vBox.Add(self.BackgroundFace())
        self.vBox.Add(self.BtnSwitch, 0, wx.LEFT | wx.EXPAND, 435)
        self.vBox.Add(self.ServerFace())
        self.vBox.AddSpacer(15)
        self.vBox.Add(self.TypeFace())
        self.vBox.Add(self.ClientFace())
        self.vBox.AddSpacer(10)
        self.vBox.Add(self.BtnUpdate, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.vBox)

    def BackgroundFace(self):
        self.ctrl = wx.adv.AnimationCtrl(self, wx.NewIdRef(), pos=(0, 0), size=(460, 80))
        gif_name = r'E:\GitHub\py3\socketDemo1\2.gif'
        self.ctrl.LoadFile(gif_name, wx.adv.ANIMATION_TYPE_GIF)
        self.ctrl.SetBackgroundColour(self.GetBackgroundColour())
        self.ctrl.Play()
        return self.ctrl

    def ServerFace(self):
        _stBox = wx.StaticBox(parent=self, id=wx.NewIdRef(), label="服务器配置")
        _stBoxS = wx.StaticBoxSizer(_stBox, wx.VERTICAL)
        _hBox = wx.BoxSizer(wx.HORIZONTAL)

        _stTextIP = wx.StaticText(self, -1, 'IP:')
        _stTextIP.SetFont(self.FT_9RNB)
        _TextIP = wx.TextCtrl(self, ID_C_SIP, '60.205.212.231')
        _TextIP.Bind(wx.EVT_KILL_FOCUS, self.CheckIP)
        _stTextPort = wx.StaticText(self, -1, '端口号:')
        _stTextPort.SetFont(self.FT_9RNB)

        _stTextUser = wx.StaticText(self, -1, '用户名:')
        _stTextUser.SetFont(self.FT_9RNB)
        _TextUser = wx.TextCtrl(self, ID_C_SUser, 'test')

        _stTextKey = wx.StaticText(self, -1, '密码:')
        _stTextKey.SetFont(self.FT_9RNB)
        _TextKey = wx.TextCtrl(self, ID_C_SKey, '123456', style=wx.TE_PASSWORD)

        _hBox.Add(_stTextIP, 1, wx.LEFT | wx.EXPAND, 5)
        _hBox.Add(_TextIP, wx.LEFT)

        _hBox.Add(_stTextUser, 1, wx.LEFT | wx.EXPAND, 10)
        _hBox.Add(_TextUser, wx.LEFT)

        _hBox.Add(_stTextKey, 1, wx.LEFT | wx.EXPAND, 10)
        _hBox.Add(_TextKey, wx.LEFT)

        _stBoxS.Add(_hBox, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        return _stBoxS

    def TypeFace(self):
        _CkBox = wx.RadioBox(self, ID_C_PkgType, '资源属性', choices=['平台', '游戏', 'Web', '其他'], size=(460, 50))
        _CkBox.SetFont(self.FT_9RNB)
        return _CkBox

    def ClientFace(self):
        _stBox = wx.StaticBox(parent=self, id=wx.NewIdRef())
        _stBoxS = wx.StaticBoxSizer(_stBox, wx.VERTICAL)
        _hBox = wx.BoxSizer(wx.HORIZONTAL)

        _TextSrc = wx.TextCtrl(self, ID_C_SrcFile, "", size=(400, 0))
        _btnFindSrc = wx.Button(self, ID_C_BtnOpenFile, "浏览...")
        _SvcList = ["正式服", "测试服", "审核服"]
        _TextSvcType = wx.ComboBox(parent=self, id=ID_C_SvcType, value="正式服", choices=_SvcList)
        _hBox.Add(_TextSvcType)
        _hBox.AddSpacer(5)
        _hBox.Add(_TextSrc, 1, wx.LEFT | wx.EXPAND, 5)
        _hBox.AddSpacer(5)
        _hBox.Add(_btnFindSrc)

        _stBoxS.Add(_hBox, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        return _stBoxS

    def GetServerInfo(self):
        _ServerIP = str(self.FindWindowById(ID_C_SIP).GetValue())
        _ServerUser = str(self.FindWindowById(ID_C_SUser).GetValue())
        _ServerKey = str(self.FindWindowById(ID_C_SKey).GetValue())
        return _ServerIP, _ServerUser, _ServerKey

    def GetSrcFile(self):
        return str(self.FindWindowById(ID_C_SrcFile).GetValue())

    def GetPkgInfo(self):
        _SvcType = str(self.FindWindowById(ID_C_SvcType).GetValue())
        _SrcType = str(self.FindWindowById(ID_C_PkgType).GetStringSelection())
        _SrcID = int(self.FindWindowById(ID_C_PkgType).GetSelection())
        return _SvcType, _SrcID, _SrcType

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


class LogPage(STC.StyledTextCtrl):
    def __init__(self, parent=None):
        self.TextStyle = STC.STC_STYLE_DEFAULT + STC.STC_STYLE_CONTROLCHAR
        super(LogPage, self).__init__(parent=parent, id=ID_C_TeLog, style=self.TextStyle)

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

    def AppendMsg(self, text):
        text = " %s\r\n" % text
        wx.CallAfter(self.AppendText, text=text)
        self.ScrollToEnd()


# TODO: 功能页
class HomePage(wx.SplitterWindow):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent=parent, id=ID_C_HomePage, size=parent.GetSize(),
                                       style=wx.SP_VERTICAL | wx.SP_NOBORDER)
        self.dialog = Dialogs(self)
        self.put = PutPage(self)
        self.log = LogPage(self)
        self.SetMinimumPaneSize(460)
        self.SplitVertically(self.put, self.log, 460)
        self.ServerPipe = None

        self.Bind(wx.EVT_BUTTON, self.OnClickSwitch, id=ID_C_BtnSwitch)
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnOpenFile, id=ID_C_BtnOpenFile)
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnSrc, id=ID_C_BtnSrc)

    def OnClickSwitch(self, e):
        curId = ID_C_BtnSwitch
        if self.FindWindowById(curId).Label == '<':
            self.FindWindowById(curId).SetLabel(">")
            self.GetParent().SetSize((460, 400))
        else:
            self.FindWindowById(curId).SetLabel("<")
            self.GetParent().SetSize((460 * 2, 400))
        e.Skip()

    def OnClickBtnOpenFile(self, e):
        if threading.activeCount() > 1:
            self.dialog.warn("有文件正在上传！")
        else:
            if self.GetParent().GetStatusBar().gauge:
                self.GetParent().GetStatusBar().gauge.SetValue(0)
            self.GetParent().GetStatusBar().SetStatusText("选择上传文件", 1)
            SrcFile = OpenFileDialog(self)
            self.FindWindowById(ID_C_SrcFile).SetValue(SrcFile)
            self.GetParent().GetStatusBar().SetStatusText("等待上传...", 1)
        return e.Skip()

    def OnClickBtnSrc(self, e):
        SrcFile = self.put.GetSrcFile()
        if not os.path.isfile(SrcFile):
            self.dialog.warn('所选文件为空或不存在!')
            self.log.AppendError('所选文件为空或不存在!')
            return e.Skip()
        self.log.AppendInfo('文件获取成功:')
        SvcType, SrcID, SrcType = self.put.GetPkgInfo()
        FileSize = os.stat(SrcFile).st_size
        srcMD5 = get_md5(SrcFile)
        self.log.AppendMsg("\t文件路径 --> \"%s\"" % SrcFile)
        self.log.AppendMsg("\t文件Size --> \"%s\"" % FileSize)
        self.log.AppendMsg("\t文件MD5值 --> \"%s\"" % srcMD5)
        self.log.AppendMsg("\t文件属性 --> \"%s\"" % SrcType)
        self.log.AppendMsg("\t服务器选择 --> \"%s\"\r" % SvcType)
        self.log.AppendInfo("准备上传%s%s资源， \"%s\"" % (SvcType, SrcType, SrcFile))
        ftpIP, ftpUser, ftpKey = self.put.GetServerInfo()
        self.bar = self.GetParent().GetStatusBar()
        self.bar.CreateGauge()
        if wx.ID_OK == self.dialog.warn("程序可能会呈现未响应状态，请勿关闭。\n\n点击确认，继续上传操作！"):
            try:
                ftp = FtpServer()
                ftp.connect(host=ftpIP, port=0, timeout=5)
                ftp.login(ftpUser, ftpKey)
                self.log.AppendInfo(ftp.getwelcome())
                # 上传
                ftp.upload(SvcType, SrcType, SrcFile, self)
            except Exception as e:
                self.dialog.error(e.__str__())
                self.log.AppendError(e.__str__())
                self.log.AppendWarn("上传资源失败!")
            finally:
                e.Skip()
        else:
            self.dialog.warn("本次上传取消!")
            self.log.AppendWarn("本次上传取消!")


class FtpServer(ftplib.FTP):
    def __init__(self):
        self.encoding = 'utf-8'
        # self.set_debuglevel(2)
        self.binaryData = [b'']
        super(FtpServer, self).__init__()

    def upload(self, svcType, srcType, filePath, parent):
        self.bar = parent.GetParent().GetStatusBar()
        self.log = parent.log
        self.dialog = parent.dialog
        self.srcMD5 = get_md5(filePath)
        self.sendSize = 0
        self.fileName = os.path.basename(filePath)
        self.fileSize = os.stat(filePath).st_size
        today = time.strftime('%Y-%m-%d/', time.localtime())
        self.workdir = svcType + '/' + today + srcType
        self.cwd('/')
        try:
            self.cwd(self.workdir)
        except Exception as e:
            self.mkd(self.workdir)
            self.cwd(self.workdir)
            self.log.AppendInfo('创建目录\"%s\"' % self.workdir)
        self.log.AppendInfo('cd %s' % self.workdir)
        if self.fileName in self.nlst() and self.size(self.fileName) == self.fileSize:
            shadowID = self.dialog.warn("已存在文件%s,确认是否重新上传？" % self.fileName)
            if shadowID == wx.ID_CANCEL:
                self.log.AppendWarn("文件已存在，取消上传")
                self.quit()
                return False
        self.fp = open(filePath, 'rb')
        t = threading.Thread(target=self.put)
        t.start()
        return True

    def put(self):
        try:
            self.storbinary(cmd="STOR %s" % self.fileName, fp=self.fp, blocksize=1024 * 1024, callback=self.freshGauge)
            self.fp.close()
        except Exception as e:
            self.log.AppendError(e.__str__())
            self.dialog.error(e.__str__())
            return False
        if self.checkSize():
            self.quit()
            self.log.AppendInfo("Ftp远端校验通过。")
            self.dialog.info("上传成功！")
            return True
        else:
            self.quit()
            self.log.AppendError("Ftp远端校验失败。")
            self.dialog.error("上传失败！")
            return False

    def freshGauge(self, buff):
        self.sendSize += len(buff)
        self.bar.SetStatusText(str(round((self.sendSize / self.fileSize) * 100, 2)) + '%', 1)
        self.bar.gauge.SetValue(round((self.sendSize / self.fileSize) * 100, 2))

    def checkSize(self):
        self.cwd('/')
        if not self.workdir:
            return False
        self.cwd(self.workdir)
        if self.fileName not in self.nlst():
            return False
        return self.size(self.fileName) == self.fileSize


class NewApp(wx.App):
    def OnInit(self):
        window = RootFrame()
        window.Show()
        return True


if __name__ == '__main__':
    freeze_support()
    app = NewApp()
    app.MainLoop()
