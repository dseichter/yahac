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
import webbrowser


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


# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details
if __name__ == "__main__":
    app = wx.App(False)
    frame = YahacFrame()
    frame.Hide()  # Start hidden, only tray icon visible
    app.MainLoop()
