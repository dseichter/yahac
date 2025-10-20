import wx

import settings
import api
import icons

import os
import sys
if sys.platform.startswith("win"):
    import win32com.client

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)

class ConfigFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Settings", size=(580, 500))
        panel = wx.Panel(self)

        # Set frame icon
        frame_icon = wx.Icon(icons.settings_24dp_1976d2_fill0_wght400_grad0_opsz24.GetIcon())
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
        
        grid.Add(wx.StaticText(panel, label=""))  # Empty label for alignment
        self.chk_confirm_state_change = wx.CheckBox(panel, label="Ask for confirmation before toggling switch")
        grid.Add(self.chk_confirm_state_change, flag=wx.LEFT, border=0)
        
        grid.Add(wx.StaticText(panel, label=""))  # Empty label for alignment
        self.chk_register_entity = wx.CheckBox(panel, label="Register yahac as a Home Assistant entity using MQTT (restart required)")
        grid.Add(self.chk_register_entity, flag=wx.LEFT, border=0)

        lbl_mqtt_host = wx.StaticText(panel, label="MQTT Host:")
        self.txt_mqtt_host = wx.TextCtrl(panel, style=wx.TE_LEFT)
        grid.Add(lbl_mqtt_host, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        grid.Add(self.txt_mqtt_host, flag=wx.EXPAND | wx.RIGHT, border=10)

        lbl_mqtt_port = wx.StaticText(panel, label="MQTT Port:")
        self.txt_mqtt_port = wx.TextCtrl(panel, style=wx.TE_LEFT)
        grid.Add(lbl_mqtt_port, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        grid.Add(self.txt_mqtt_port, flag=wx.EXPAND | wx.RIGHT, border=10)
        
        lbl_mqtt_user = wx.StaticText(panel, label="MQTT User:")
        self.txt_mqtt_user = wx.TextCtrl(panel, style=wx.TE_LEFT)
        grid.Add(lbl_mqtt_user, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        grid.Add(self.txt_mqtt_user, flag=wx.EXPAND | wx.RIGHT, border=10)
        
        lbl_mqtt_password = wx.StaticText(panel, label="MQTT Password:")
        self.txt_mqtt_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        grid.Add(lbl_mqtt_password, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        grid.Add(self.txt_mqtt_password, flag=wx.EXPAND | wx.RIGHT, border=10)

        # Log Level
        lbl_log_level = wx.StaticText(panel, label="Log Level:")
        self.cmb_log_level = wx.ComboBox(panel, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.cmb_log_level.Append("DEBUG")
        self.cmb_log_level.Append("INFO")
        self.cmb_log_level.Append("ERROR")
        grid.Add(lbl_log_level, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        grid.Add(self.cmb_log_level, flag=wx.EXPAND | wx.RIGHT, border=10)

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
        self.chk_autostart.Bind(wx.EVT_CHECKBOX, self.set_autostart)
        self.token_visible = False

        self.load_settings()

    def load_settings(self):
        url = settings.load_value_from_json_file("url")
        token = settings.load_value_from_json_file("token")
        checkupdate = settings.load_value_from_json_file("checkupdate")
        autostart = settings.load_value_from_json_file("autostart")
        confirm_state_change = settings.load_value_from_json_file('confirm_state_change')
        register_entity = settings.load_value_from_json_file('register_entity')
        mqtt_host = settings.load_value_from_json_file("mqtt_host")
        mqtt_port = settings.load_value_from_json_file("mqtt_port")
        mqtt_user = settings.load_value_from_json_file("mqtt_user")
        mqtt_password = settings.load_value_from_json_file("mqtt_password")
        log_level = settings.load_value_from_json_file("loglevel")

        self.txt_url.SetValue(url if url else "")
        self.txt_token.SetValue(token if token else "")
        self.chk_checkupdate.SetValue(bool(checkupdate))
        self.chk_autostart.SetValue(bool(autostart))
        self.chk_confirm_state_change.SetValue(bool(confirm_state_change))
        self.chk_register_entity.SetValue(bool(register_entity))
        self.txt_mqtt_host.SetValue(mqtt_host if mqtt_host else "")
        self.txt_mqtt_port.SetValue(str(mqtt_port) if mqtt_port else "")
        self.txt_mqtt_user.SetValue(mqtt_user if mqtt_user else "")
        self.txt_mqtt_password.SetValue(mqtt_password if mqtt_password else "")
        self.cmb_log_level.SetValue(log_level if log_level else "INFO")
        
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
        confirm_state_change = self.chk_confirm_state_change.GetValue()
        register_entity = self.chk_register_entity.GetValue()
        # Save logic placeholder
        settings.save_config("url", url)
        settings.save_config("token", token)
        settings.save_config("checkupdate", checkupdate)
        settings.save_config("autostart", autostart)
        settings.save_config('confirm_state_change', confirm_state_change)
        settings.save_config('register_entity', register_entity)
        settings.save_config("mqtt_host", self.txt_mqtt_host.GetValue())
        settings.save_config("mqtt_port", int(self.txt_mqtt_port.GetValue()) if self.txt_mqtt_port.GetValue().isdigit() else 0)
        settings.save_config("mqtt_user", self.txt_mqtt_user.GetValue())
        settings.save_config("mqtt_password", self.txt_mqtt_password.GetValue())
        settings.save_config("loglevel", self.cmb_log_level.GetValue())

        wx.MessageBox("Settings saved.", "Save", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def on_cancel(self, event):
        self.Close()

    def set_autostart(self, event):
        autostart = self.chk_autostart.GetValue()
        logger.info(f"Setting autostart to: {autostart}")
        app_name = "yahac"
        exe_path = sys.executable if getattr(sys, "frozen", False) else sys.argv[0]
        # Validate and sanitize the executable path
        exe_path = os.path.abspath(os.path.normpath(exe_path))
        if not os.path.exists(exe_path) or ".." in exe_path:
            logger.error(f"Invalid executable path: {exe_path}")
            return
        if sys.platform.startswith("win"):
            
            startup_dir = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            shortcut_path = os.path.join(startup_dir, f"{app_name}.lnk")
            shell = win32com.client.Dispatch("WScript.Shell")
            if autostart:
                shortcut = shell.CreateShortcut(shortcut_path)
                shortcut.TargetPath = exe_path
                shortcut.WorkingDirectory = os.path.dirname(exe_path)
                shortcut.IconLocation = exe_path
                shortcut.Save()
            else:
                if os.path.exists(shortcut_path):
                    os.remove(shortcut_path)
        elif sys.platform.startswith("linux"):
            # Untested!!!
            autostart_dir = os.path.expanduser("~/.config/autostart")
            os.makedirs(autostart_dir, exist_ok=True)
            desktop_path = os.path.join(autostart_dir, f"{app_name}.desktop")
            if autostart:
                desktop_entry = f"""[Desktop Entry]
Type=Application
Exec={exe_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name={app_name}
Comment=Autostart {app_name}
"""
                with open(desktop_path, "w", encoding="utf-8") as f:
                    f.write(desktop_entry)
            else:
                if os.path.exists(desktop_path):
                    os.remove(desktop_path)
