import wx

class ConfigFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Settings", size=(350, 220))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # URL
        hbox_url = wx.BoxSizer(wx.HORIZONTAL)
        lbl_url = wx.StaticText(panel, label="URL:")
        self.txt_url = wx.TextCtrl(panel)
        hbox_url.Add(lbl_url, flag=wx.RIGHT, border=8)
        hbox_url.Add(self.txt_url, proportion=1)
        vbox.Add(hbox_url, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Token
        hbox_token = wx.BoxSizer(wx.HORIZONTAL)
        lbl_token = wx.StaticText(panel, label="Token:")
        self.txt_token = wx.TextCtrl(panel)
        hbox_token.Add(lbl_token, flag=wx.RIGHT, border=8)
        hbox_token.Add(self.txt_token, proportion=1)
        vbox.Add(hbox_token, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Buttons
        hbox_btn = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_test = wx.Button(panel, label="Test")
        self.btn_save = wx.Button(panel, label="Save")
        self.btn_cancel = wx.Button(panel, label="Cancel")
        hbox_btn.Add(self.btn_test, flag=wx.RIGHT, border=5)
        hbox_btn.Add(self.btn_save, flag=wx.RIGHT, border=5)
        hbox_btn.Add(self.btn_cancel)
        vbox.Add(hbox_btn, flag=wx.ALIGN_RIGHT|wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.btn_test.Bind(wx.EVT_BUTTON, self.on_test)
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_test(self, event):
        url = self.txt_url.GetValue()
        token = self.txt_token.GetValue()
        # Dummy test logic
        if url and token:
            wx.MessageBox("Test successful!", "Test", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Please provide both URL and Token.", "Test", wx.OK | wx.ICON_WARNING)

    def on_save(self, event):
        url = self.txt_url.GetValue()
        token = self.txt_token.GetValue()
        # Save logic placeholder
        wx.MessageBox("Settings saved.", "Save", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def on_cancel(self, event):
        self.Close()

class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        icon = wx.Icon(wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16)))
        self.SetIcon(icon, "YAHAC")
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.on_menu)


    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(1, "Sensors", "Your selected sensors", kind=wx.ITEM_NORMAL)
        menu.AppendSeparator()
        menu.AppendSeparator()
        menu.Append(2, "Sensors", "Manage your sensors")
        menu.Append(3, "Settings", "Configure connection to your Home Assistant")
        menu.AppendSeparator()
        menu.Append(4, "Exit")
        self.Bind(wx.EVT_MENU, self.on_show, id=1)
        self.Bind(wx.EVT_MENU, self.on_sensors, id=3)
        self.Bind(wx.EVT_MENU, self.on_settings, id=3)
        self.Bind(wx.EVT_MENU, self.on_exit, id=4)
        return menu

    def on_menu(self, event):
        self.PopupMenu(self.CreatePopupMenu())

    def on_show(self, event):
        self.frame.Show()
        self.frame.Raise()

    def on_sensors(self, event):
        if hasattr(self.frame, "on_sensors"):
            self.frame.on_sensors(event)

    def on_settings(self, event):
        if hasattr(self.frame, "on_settings"):
            self.frame.on_settings(event)

    def on_exit(self, event):
        wx.CallAfter(self.frame.Close)

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="YAHAC", size=(300, 200))
        self.tray_icon = TrayIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)


    def on_close(self, event):
        self.tray_icon.RemoveIcon()
        self.tray_icon.Destroy()
        self.Destroy()

