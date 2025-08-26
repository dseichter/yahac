import wx

class ConfigFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Settings", size=(350, 220))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Set frame icon
        frame_icon = wx.Icon(wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, (16, 16)))
        self.SetIcon(frame_icon)

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

