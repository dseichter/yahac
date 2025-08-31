import wx

import wx.adv
import gui_traymenu
import gui_config
import settings


import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="YAHAC", size=(300, 200))
        self.tray_icon = gui_traymenu.TrayIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Check, if settings are available
        if not settings.CONFIGFILE:
            logger.warning("Configuration file not found. Creating default configuration.")
            settings.create_config()

        # Load configuration and check, if url and token is set. If not, Show message
        config = settings.read_config()
        if not config.get("url") or not config.get("token"):
            logger.warning("URL and token must be set in the configuration.")
            # Show message to user
            wx.MessageBox("Please set the URL and token in the configuration.", "Missing Configuration", wx.OK | wx.ICON_WARNING)
            config_frame = gui_config.ConfigFrame(self)
            logger.info("Showing settings dialog")
            config_frame.Show()

    def on_close(self, event):
        self.tray_icon.RemoveIcon()
        self.tray_icon.Destroy()
        self.Destroy()
