import wx

import wx.adv
import gui_config
import gui_sensors
import settings


class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        icon = wx.Icon(wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16)))
        self.SetIcon(icon, "YAHAC")
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.on_menu)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(1, "Your Sensors:", "Your selected sensors:", kind=wx.ITEM_NORMAL)
        menu.AppendSeparator()
        # Dynamic generation of sensor/switch - start
        self.load_sensors(menu)
        # Dynamic generation of sensor/switch - end
        menu.AppendSeparator()
        # Sensors menu item
        sensors_item = wx.MenuItem(menu, 2, "Sensors", "Manage your sensors")
        sensors_icon = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_MENU, (16, 16))
        sensors_item.SetBitmap(sensors_icon)
        menu.Append(sensors_item)
        # Settings menu item
        settings_item = wx.MenuItem(menu, 3, "Settings", "Configure connection to your Home Assistant")
        settings_icon = wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_MENU, (16, 16))
        settings_item.SetBitmap(settings_icon)
        menu.Append(settings_item)

        menu.AppendSeparator()
        # Settings menu item
        exit_item = wx.MenuItem(menu, 4, "Exit", "Exit the application")
        exit_icon = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU, (16, 16))
        exit_item.SetBitmap(exit_icon)
        menu.Append(exit_item)
        self.Bind(wx.EVT_MENU, self.on_sensors, id=2)
        self.Bind(wx.EVT_MENU, self.on_settings, id=3)
        self.Bind(wx.EVT_MENU, self.on_exit, id=4)
        return menu

    def on_menu(self, event):
        self.PopupMenu(self.CreatePopupMenu())

    def on_sensors(self, event):
        sensors_frame = gui_sensors.SensorSelectorFrame(self.frame)
        print("Showing sensors dialog")
        sensors_frame.Show()

    def on_settings(self, event):
        config_frame = gui_config.ConfigFrame(self.frame)
        print("Showing settings dialog")
        config_frame.Show()

    def on_exit(self, event):
        wx.CallAfter(self.frame.Close)

    def load_sensors(self, menu):
        sensors = settings.load_value_from_json_file("entities")
        if not sensors:
            return
        for sensor in sensors:
            entity_id = sensor.get("entity_id", "")
            friendly_name = sensor.get("friendly_name", entity_id)
            entity_type = sensor.get("type", "switch")
            # Add to the UI or internal list
            print(f"Loaded sensor: {friendly_name} ({entity_id}) - {entity_type}")
            if entity_type == "sensor":
                sensor_item = menu.Append(wx.ID_ANY, friendly_name, helpString=entity_id, kind=wx.ITEM_NORMAL)
                sensor_icon = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MENU, (16, 16))
                sensor_item.SetBitmap(sensor_icon)
            if entity_type == "switch":
                switch_item = menu.Append(wx.ID_ANY, friendly_name, helpString=entity_id, kind=wx.ITEM_CHECK)
                switch_icon = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_MENU, (16, 16))  # TODO: find appropriate icon
                switch_item.SetBitmap(switch_icon)
                # self.Bind(wx.EVT_MENU, self.on_switch_selected, id=switch_item.GetId())

    def on_switch_selected(self, event):
        item = self.GetPopupMenuSelection()
        if item:
            print(f"Switch selected: {item.GetItemLabelText()}")
