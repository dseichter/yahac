import wx

import wx.adv
import gui_traymenu

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="YAHAC", size=(300, 200))
        self.tray_icon = gui_traymenu.TrayIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)


    def on_close(self, event):
        self.tray_icon.RemoveIcon()
        self.tray_icon.Destroy()
        self.Destroy()
