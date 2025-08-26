import wx

entities = [
       "dummy.sensor"
    ]

class SensorSelectorFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Select Entity", size=(400, 120))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Set frame icon
        frame_icon = wx.Icon(wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, (16, 16)))
        self.SetIcon(frame_icon)

        label = wx.StaticText(panel, label="Choose an entity:")
        vbox.Add(label, flag=wx.LEFT | wx.TOP, border=10)

        self.combobox = wx.ComboBox(
            panel,
            choices=entities,
            style=wx.CB_DROPDOWN | wx.CB_SORT
        )
        vbox.Add(self.combobox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        panel.SetSizer(vbox)

        # Enable typing/searching in the combobox
        self.combobox.Bind(wx.EVT_TEXT, self.on_search)

    def on_search(self, event):
        # Optionally, implement live filtering here
        pass

