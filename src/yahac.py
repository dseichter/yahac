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
import gui

class YahacFrame(gui.MainFrame):
    # constructor
    def __init__(self):
        # initialize parent class
        gui.MainFrame.__init__(self)

    def on_settings(self, event):
        config_frame = gui.ConfigFrame(self)
        print("Showing settings dialog")
        config_frame.Show()
        

# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details
if __name__ == "__main__":
    app = wx.App(False)
    frame = YahacFrame()
    frame.Hide()  # Start hidden, only tray icon visible
    app.MainLoop()
