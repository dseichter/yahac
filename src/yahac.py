# Copyright (c) 2025 Daniel Seichter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# importing wx files
import wx
import wx.adv

# import the newly created GUI file
import gui_mainframe
import settings
import helper
import ha_helper
import webbrowser

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)


class YahacFrame(gui_mainframe.MainFrame):
    # constructor
    def __init__(self):
        # initialize parent class
        gui_mainframe.MainFrame.__init__(self)
        settings.create_config()
        # Check for update if enabled
        if settings.load_value_from_json_file("checkupdate"):
            if helper.check_for_new_release():
                result = wx.MessageBox(
                    "A new release is available.\nWould you like to open the download page?",
                    "Update available",
                    wx.YES_NO | wx.ICON_INFORMATION,
                )
                if result == wx.YES:
                    webbrowser.open_new_tab(helper.RELEASES)

        if settings.load_value_from_json_file("register_entity"):
            # hack: before setting the entity online, set it offline first to be able to trigger the state change
            logger.info("Set entity offline first to be able to trigger the state change.")
            ha_helper.set_entity_state_offline()
            logger.info("Create timer and set entity state online.")
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
            self.timer.Start(5000)  # Check every 5 seconds
        else:
            logger.info("Remove the entity from Home Assistant, if config is disabling the integration.")
            ha_helper.set_entity_state_offline()

    def on_timer(self, event):
        ha_helper.set_entity_state_online()

    def on_close(self, event):
        # set entity offline, if enabled
        if settings.load_value_from_json_file("register_entity"):
            logger.info("Set entity state to offline on close.")
            ha_helper.set_entity_state_offline()
        # call parent close method
        gui_mainframe.MainFrame.on_close(self, event)


# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details
if __name__ == "__main__":
    app = wx.App(False)
    frame = YahacFrame()
    frame.Hide()  # Start hidden, only tray icon visible
    app.MainLoop()
