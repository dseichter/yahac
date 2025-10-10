import wx

import wx.adv
import gui_config
import gui_sensors
import settings
import helper
import webbrowser
import api
import icons

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)

class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        icon = icons.home_app_logo_24dp_1976d2_fill0_wght400_grad0_opsz24.GetIcon()
        self.SetIcon(icon, "YAHAC")
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.on_menu)
        
        # Build the mapping of the sensors, to be used for interactive elements, like switches
        self.menu_id_map = {}

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(1, f"{helper.NAME} {helper.VERSION}", kind=wx.ITEM_NORMAL)
        menu.AppendSeparator()
        # Dynamic generation of sensor/switch - start
        self.load_sensors(menu)
        # Dynamic generation of sensor/switch - end
        menu.AppendSeparator()
        # Sensors menu item
        sensors_item = wx.MenuItem(menu, 2, "Sensors", "Manage your sensors")
        sensors_icon = icons.database_24dp_1976d2_fill0_wght400_grad0_opsz24.GetBitmap()
        sensors_item.SetBitmap(sensors_icon)
        menu.Append(sensors_item)
        # Settings menu item
        settings_item = wx.MenuItem(menu, 3, "Settings", "Configure connection to your Home Assistant")
        settings_icon = icons.settings_24dp_1976d2_fill0_wght400_grad0_opsz24.GetBitmap()
        settings_item.SetBitmap(settings_icon)
        menu.Append(settings_item)

        # Check for update
        checkupdate_item = wx.MenuItem(menu, 5, "Check for update...", "Check for new version")
        update_icon = icons.update_24dp_1976d2_fill0_wght400_grad0_opsz24.GetBitmap()
        checkupdate_item.SetBitmap(update_icon)
        menu.Append(checkupdate_item)
        self.Bind(wx.EVT_MENU, self.on_check_update, id=5)

        # Open Webpage/Repository/Documentation
        webpage_item = wx.MenuItem(menu, 6, "Open Documentation", "Open the project's webpage or repository")
        update_icon = icons.globe_24dp_1976d2_fill0_wght400_grad0_opsz24.GetBitmap()
        webpage_item.SetBitmap(update_icon)
        menu.Append(webpage_item)
        self.Bind(wx.EVT_MENU, self.on_webpage_open, id=6)

        menu.AppendSeparator()
        # Settings menu item
        exit_item = wx.MenuItem(menu, 4, "Exit", "Exit the application")
        exit_icon = icons.logout_24dp_1976d2_fill0_wght400_grad0_opsz24.GetBitmap()
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
        logger.info("Showing sensors dialog")
        sensors_frame.Show()

    def on_settings(self, event):
        config_frame = gui_config.ConfigFrame(self.frame)
        logger.info("Showing settings dialog")
        config_frame.Show()
        
    def on_check_update(self, event):
        if helper.check_for_new_release():
            result = wx.MessageBox(
                "A new release is available.\nWould you like to open the download page?",
                "Update available",
                wx.YES_NO | wx.ICON_INFORMATION,
            )
            if result == wx.YES:
                webbrowser.open_new_tab(helper.RELEASES)
        else:
            wx.MessageBox("No new release available.", "No update", wx.OK | wx.ICON_INFORMATION)

    def on_webpage_open(self, event):
        webbrowser.open_new_tab(helper.WEBSITE)

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
            entity_state = api.get_entity_state(entity_id)
            logger.info(f"Loaded sensor: {friendly_name} ({entity_id}) - {entity_type} - {entity_state}")
            if entity_type == "sensor":
                sensor_icon = icons.sensors_24dp_1976d2_fill0_wght400_grad0_opsz24.GetBitmap()
                sensor_item = wx.MenuItem(menu, wx.ID_ANY, f"{friendly_name} ({entity_state})", helpString=entity_id)
                sensor_item.SetBitmap(sensor_icon)
                menu.Append(sensor_item)
                self.menu_id_map[sensor_item.GetId()] = sensor
                self.Bind(wx.EVT_MENU, self.on_sensor_selected, id=sensor_item.GetId())
            if entity_type == "switch":
                if entity_state == "on":
                    switch_icon = icons.toggle_on_24dp_1976d2_fill0_wght400_grad0_opsz24.GetBitmap()
                else:
                    switch_icon = icons.toggle_off_24dp_1976d2_fill0_wght400_grad0_opsz24.GetBitmap()
                switch_item = wx.MenuItem(menu, wx.ID_ANY, f"{friendly_name} ({entity_state})", helpString=entity_id)
                switch_item.SetBitmap(switch_icon)
                menu.Append(switch_item)
                self.menu_id_map[switch_item.GetId()] = sensor
                self.Bind(wx.EVT_MENU, self.on_switch_selected, id=switch_item.GetId())

    def on_sensor_selected(self, event):
        sensor = self.menu_id_map.get(event.GetId())
        if sensor:
            logger.info(f"Sensor selected: {sensor['friendly_name']} ({sensor['entity_id']})")

    def on_switch_selected(self, event):
        switch = self.menu_id_map.get(event.GetId())
        if switch:
            current_state = api.get_entity_state(switch['entity_id'])

            new_state = "off" if current_state == "on" else "on"
            confirm_state_change = settings.load_value_from_json_file("confirm_state_change")
            if confirm_state_change:
                confirmation = wx.MessageBox(f"Toggle {switch['friendly_name']} from {current_state} to {new_state}?", "Confirm", wx.YES_NO | wx.ICON_QUESTION)
                if confirmation == wx.YES:
                    confirm_state_change = False

            # only, if confirm_state_change is False
            if not confirm_state_change:
                success = api.set_entity_switch_state(switch['entity_id'], new_state)
                if success:
                    logger.info(f"Switch {switch['friendly_name']} ({switch['entity_id']}) set to {new_state.upper()}")
                else:
                    wx.MessageBox(f"Failed to set {switch['friendly_name']} ({switch['entity_id']}) to {new_state.upper()}", "Error", wx.OK | wx.ICON_ERROR)
                    logger.info(f"Failed to set switch {switch['friendly_name']} ({switch['entity_id']}) to {new_state.upper()}")
