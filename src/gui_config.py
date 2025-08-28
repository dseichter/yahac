import wx

import settings
import api
import os
import sys


class ConfigFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Settings", size=(400, 220))
        panel = wx.Panel(self)

        # Set frame icon
        frame_icon = wx.Icon(wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, (16, 16)))
        self.SetIcon(frame_icon)
        # Use FlexGridSizer for two columns
        grid = wx.FlexGridSizer(rows=0, cols=2, vgap=10, hgap=10)
        grid.AddGrowableCol(1, 1)

        # URL
        lbl_url = wx.StaticText(panel, label="URL:")
        self.txt_url = wx.TextCtrl(panel, style=wx.TE_LEFT)
        grid.Add(lbl_url, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        grid.Add(self.txt_url, flag=wx.EXPAND | wx.RIGHT, border=10)

        # Token (secret) + Show button
        lbl_token = wx.StaticText(panel, label="Token:")
        hbox_token = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_token = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        self.btn_show_token = wx.Button(panel, label="Show", size=(60, -1))
        hbox_token.Add(self.txt_token, proportion=1, flag=wx.EXPAND)
        hbox_token.Add(self.btn_show_token, flag=wx.LEFT, border=5)
        grid.Add(lbl_token, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        grid.Add(hbox_token, flag=wx.EXPAND | wx.RIGHT, border=10)

        # Checkboxes
        grid.Add(wx.StaticText(panel, label=""))  # Empty label for alignment
        self.chk_checkupdate = wx.CheckBox(panel, label="Update on startup")
        grid.Add(self.chk_checkupdate, flag=wx.LEFT, border=0)

        grid.Add(wx.StaticText(panel, label=""))  # Empty label for alignment
        self.chk_autostart = wx.CheckBox(panel, label="Autostart application")
        grid.Add(self.chk_autostart, flag=wx.LEFT, border=0)

        # Buttons (span two columns)
        hbox_btn = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_test = wx.Button(panel, label="Test")
        self.btn_save = wx.Button(panel, label="Save")
        self.btn_cancel = wx.Button(panel, label="Cancel")
        hbox_btn.Add(self.btn_test, flag=wx.RIGHT, border=10)
        hbox_btn.Add(self.btn_save, flag=wx.RIGHT, border=10)
        hbox_btn.Add(self.btn_cancel, flag=wx.RIGHT, border=0)
        grid.AddSpacer(0)  # Fills the first column for alignment
        grid.Add(hbox_btn, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)
        

        panel.SetSizer(grid)

        self.btn_show_token.Bind(wx.EVT_BUTTON, self.on_show_token)
        self.btn_test.Bind(wx.EVT_BUTTON, self.on_test)
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.token_visible = False

        self.load_settings()

    def load_settings(self):
        url = settings.load_value_from_json_file('url')
        token = settings.load_value_from_json_file('token')
        checkupdate = settings.load_value_from_json_file('checkupdate')
        autostart = settings.load_value_from_json_file('autostart')

        self.txt_url.SetValue(url if url else "")
        self.txt_token.SetValue(token if token else "")
        self.chk_checkupdate.SetValue(bool(checkupdate))
        self.chk_autostart.SetValue(bool(autostart))        

    def on_show_token(self, _event):
        current_value = self.txt_token.GetValue()
        if self.token_visible:
            self.txt_token.SetWindowStyle(wx.TE_PASSWORD)
            self.btn_show_token.SetLabel("Show")
            self.token_visible = False
        else:
            self.txt_token.SetWindowStyle(wx.TE_PROCESS_ENTER)
            self.btn_show_token.SetLabel("Hide")
            self.token_visible = True
        # Re-set the value to force a refresh
        self.txt_token.ChangeValue(current_value)

    def on_test(self, event):
        url = self.txt_url.GetValue()
        token = self.txt_token.GetValue()
        if url and token:
            result = api.check_connection(url, token)
            wx.MessageBox(result, "Test", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Please provide both URL and Token.", "Test", wx.OK | wx.ICON_WARNING)

    def on_save(self, event):
        url = self.txt_url.GetValue()
        token = self.txt_token.GetValue()
        checkupdate = self.chk_checkupdate.GetValue()
        autostart = self.chk_autostart.GetValue()
        # Save logic placeholder
        settings.save_config('url', url)
        settings.save_config('token', token)
        settings.save_config('checkupdate', checkupdate)
        settings.save_config('autostart', autostart)

        wx.MessageBox("Settings saved.", "Save", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def on_cancel(self, event):
        self.Close()

    def set_autostart(self, autostart):
        app_name = "yahac"
        startup_dir = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        shortcut_path = os.path.join(startup_dir, f"{app_name}.lnk")
        
        if autostart:
            # Code to enable autostart
            exe_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
            try:
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = exe_path
                shortcut.WorkingDirectory = os.path.dirname(exe_path)
                shortcut.IconLocation = exe_path
                shortcut.save()
            except Exception as e:
                wx.MessageBox(f"Failed to enable autostart: {e}", "Autostart", wx.OK | wx.ICON_ERROR)
        else:
            # Code to disable autostart
            try:
                if os.path.exists(shortcut_path):
                    os.remove(shortcut_path)
            except Exception as e:
                wx.MessageBox(f"Failed to disable autostart: {e}", "Autostart", wx.OK | wx.ICON_ERROR)
