import wx.stc as STC
import wx, wx.adv, wx.grid, wx.ribbon
import wx.lib.agw.customtreectrl as CT
from multiprocessing import freeze_support


# TODO: 主框架
class RootFrame(wx.Frame):
    def __init__(self, parent=None):
        super(RootFrame, self).__init__(parent=parent, id=wx.NewId(), style=wx.DEFAULT_FRAME_STYLE)
        self.settings()
        wx.CallAfter(self.initUI)

    def settings(self):
        self.SetTitle(u'客户端更新工具')
        self.SetSize((480, 360))
        self.SetMaxClientSize((480, 360))
        self.SetMinClientSize((480, 360))
        self.SetTransparent(230)
        self.TaskBarIcon = None
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        # self.SetIcon(PyEmbeddedImage(B64_POKER128).GetIcon())
        self.Center()

    def initUI(self):
        # MenuBar(self)
        MidWindow(self)
        StatusBar(self)


class MenuBar(wx.MenuBar):
    def __init__(self, parent=None):
        super(MenuBar, self).__init__()
        FileMenu = wx.Menu()
        OptionMenu = wx.Menu()
        ViewMenu = wx.Menu()
        HelpMenu = wx.Menu()
        self.Append(FileMenu, u'文件(&F)')
        self.Append(OptionMenu, u'选项(&O)')
        self.Append(ViewMenu, u'查看(&H)')
        self.Append(HelpMenu, u'帮助(&H)')
        parent.SetMenuBar(self)

    def setItems(self):
        pass


# TODO: 主界面
class MidWindow(wx.Panel):
    def __init__(self, parent=None, id=wx.NewId()):
        super(MidWindow, self).__init__(parent=parent, id=id, name='Main', size=parent.GetSize())
        self.initUI()

    def initUI(self):
        font_9b = wx.Font(9, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        vBox = wx.BoxSizer(wx.VERTICAL)
        stBox1 = wx.StaticBox(parent=self, id=wx.NewId(), label='服务端设置', size=self.GetSize())
        stBoxS1 = wx.StaticBoxSizer(stBox1, wx.VERTICAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        st_sip = wx.StaticText(self, -1, "IP：")
        st_sip.SetFont(font_9b)
        t_sip = wx.TextCtrl(self, -1, "192.168.1.18")
        st_sport = wx.StaticText(self, -1, "端口号：")
        st_sport.SetFont(font_9b)
        t_sport = wx.TextCtrl(self, -1, "5000", size=(40, t_sip.GetSize()[1]))
        st_key = wx.StaticText(self, -1, "口令：")
        st_key.SetFont(font_9b)
        t_key = wx.TextCtrl(self, -1, "123456", size=(98, t_sip.GetSize()[1]))

        btn_test = wx.Button(self, -1, "测试连接")
        hBox1.Add(st_sip)
        hBox1.Add(t_sip)
        hBox1.AddSpacer(6)
        hBox1.Add(st_sport)
        hBox1.Add(t_sport)
        hBox1.AddSpacer(6)
        hBox1.Add(st_key)
        hBox1.Add(t_key)
        hBox1.AddSpacer(6)
        hBox1.Add(btn_test)

        stBox2 = wx.StaticBox(parent=self, id=wx.NewId(), label='更新设置', size=self.GetSize(), pos=(100, 100))
        stBoxS2 = wx.StaticBoxSizer(stBox2, wx.VERTICAL)

        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        st_ip = wx.StaticText(self, -1, "服务器：")
        st_ip.SetFont(font_9b)
        t_ip = wx.TextCtrl(self, -1, "192.168.1.13")

        st_id = wx.StaticText(self, -1, "游戏代号：")
        st_id.SetFont(font_9b)
        GameList = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010", "1011", "1012",
                    "1013", "1014", "1015", "1016", "1017", "1018", "1019", "1020", "1021", "1022", "1023", "1024",
                    "1025", "1026"]
        cBox_id = wx.ComboBox(parent=self, id=-1, value="1001", choices=GameList)

        st_type = wx.StaticText(self, -1, "客户端类型：")
        st_type.SetFont(font_9b)
        cBox = wx.ComboBox(parent=self, id=-1, value="热更新包", choices=["热更新包", "整包"], style=wx.CB_READONLY)

        hBox2.Add(st_ip)
        hBox2.Add(t_ip)
        hBox2.AddSpacer(14)

        hBox2.Add(st_id)
        hBox2.Add(cBox_id)
        hBox2.AddSpacer(14)

        hBox2.Add(st_type)
        hBox2.Add(cBox)

        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        t_src = wx.TextCtrl(self, -1, "", size=(370, t_sip.GetSize()[1]))
        btn_src = wx.Button(self, -1, "资源上传...")

        hBox3.Add(t_src)
        hBox3.Add(btn_src)

        stBoxS1.AddSpacer(20)
        stBoxS1.Add(hBox1)
        stBoxS1.AddSpacer(20)

        stBoxS2.AddSpacer(20)
        stBoxS2.Add(hBox2)
        stBoxS2.AddSpacer(20)
        stBoxS2.Add(hBox3)
        stBoxS2.AddSpacer(20)

        btn_update = wx.Button(self, -1, "更    新")
        font_29b = wx.Font(29, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        btn_update.SetFont(font_29b)
        btn_update.SetForegroundColour(wx.BLUE)

        vBox.Add(stBoxS1)
        vBox.AddSpacer(20)
        vBox.Add(stBoxS2)
        vBox.Add(btn_update, 1, wx.ALL | wx.EXPAND, 15)

        self.SetSizer(vBox)


# TODO: 状态栏
class StatusBar(wx.StatusBar):
    def __init__(self, parent=None, id=wx.NewId()):
        super(StatusBar, self).__init__(parent=parent, id=id, style=65840, name=u'状态栏')
        self.SetFieldsCount(3)
        self.SetStatusWidths([-2, -2, -1])
        self.Show()
        if parent:
            parent.SetStatusBar(self)


# TODO: 主进程
class NewApp(wx.App):
    def OnInit(self):
        window = RootFrame()
        window.Show()
        return True


if __name__ == '__main__':
    # 多进程打包支持
    freeze_support()
    app = NewApp()
    app.MainLoop()
