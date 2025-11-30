from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox, QApplication
from PySide6.QtGui import QAction

import gui_config
import gui_sensors
import settings
import helper
import webbrowser
import api
import icons as icons

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Store references to open dialogs
        self.sensors_dialog = None
        self.config_dialog = None
        
        # Set tray icon
        icon = icons.get_icon('home_app_logo_24dp_1976d2_fill0_wght400_grad0_opsz24')
        self.setIcon(icon)
        self.setToolTip("YAHAC")
        
        # Create context menu
        self.create_menu()
        
        # Show tray icon
        self.show()
        
        # Connect signals
        self.activated.connect(self.on_tray_activated)
        
        # Build the mapping of the sensors for interactive elements
        self.menu_id_map = {}

    def create_menu(self):
        menu = QMenu()
        
        # Title
        title_action = QAction(f"{helper.NAME} {helper.VERSION}", self)
        title_action.setEnabled(False)
        menu.addAction(title_action)
        menu.addSeparator()
        
        # Dynamic sensors/switches
        self.load_sensors(menu)
        menu.addSeparator()
        
        # Sensors menu item
        sensors_action = QAction("Sensors", self)
        sensors_action.setIcon(icons.get_icon('database_24dp_1976d2_fill0_wght400_grad0_opsz24'))
        sensors_action.setToolTip("Manage your sensors")
        sensors_action.triggered.connect(self.on_sensors)
        menu.addAction(sensors_action)
        
        # Settings menu item
        settings_action = QAction("Settings", self)
        settings_action.setIcon(icons.get_icon('settings_24dp_1976d2_fill0_wght400_grad0_opsz24'))
        settings_action.setToolTip("Configure connection to your Home Assistant")
        settings_action.triggered.connect(self.on_settings)
        menu.addAction(settings_action)
        
        # Check for update
        update_action = QAction("Check for update...", self)
        update_action.setIcon(icons.get_icon('update_24dp_1976d2_fill0_wght400_grad0_opsz24'))
        update_action.setToolTip("Check for new version")
        update_action.triggered.connect(self.on_check_update)
        menu.addAction(update_action)
        
        # Open Documentation
        docs_action = QAction("Open Documentation", self)
        docs_action.setIcon(icons.get_icon('globe_24dp_1976d2_fill0_wght400_grad0_opsz24'))
        docs_action.setToolTip("Open the project's webpage or repository")
        docs_action.triggered.connect(self.on_webpage_open)
        menu.addAction(docs_action)
        
        menu.addSeparator()
        
        # Exit
        exit_action = QAction("Exit", self)
        exit_action.setIcon(icons.get_icon('logout_24dp_1976d2_fill0_wght400_grad0_opsz24'))
        exit_action.setToolTip("Exit the application")
        exit_action.triggered.connect(self.on_exit)
        menu.addAction(exit_action)
        
        self.setContextMenu(menu)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Context:
            # Refresh menu before showing
            self.create_menu()

    def on_sensors(self):
        """Open the sensor selection dialog and reload sensors after closing."""
        if self.sensors_dialog is None or not self.sensors_dialog.isVisible():
            self.sensors_dialog = gui_sensors.SensorSelectorDialog(self.parent)
            logger.info("Showing sensors dialog")
            self.sensors_dialog.exec()
            self.sensors_dialog = None
            # Reload menu after sensor dialog closes
            logger.info("Reloading sensors after dialog close")
            self.create_menu()
        else:
            logger.info("Sensors dialog already open")
            self.sensors_dialog.raise_()
            self.sensors_dialog.activateWindow()

    def on_settings(self):
        """Open the settings configuration dialog."""
        if self.config_dialog is None or not self.config_dialog.isVisible():
            self.config_dialog = gui_config.ConfigDialog(self.parent)
            logger.info("Showing settings dialog")
            self.config_dialog.exec()
            self.config_dialog = None
        else:
            logger.info("Settings dialog already open")
            self.config_dialog.raise_()
            self.config_dialog.activateWindow()

    def on_check_update(self):
        """Check for application updates and prompt user to download if available."""
        if helper.check_for_new_release():
            reply = QMessageBox.question(
                self.parent,
                "Update available",
                "A new release is available.\nWould you like to open the download page?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                webbrowser.open_new_tab(helper.RELEASES)
        else:
            QMessageBox.information(
                self.parent,
                "No update",
                "No new release available."
            )

    def on_webpage_open(self):
        webbrowser.open_new_tab(helper.WEBSITE)

    def on_exit(self):
        self.parent.close()
        QApplication.instance().quit()

    def load_sensors(self, menu):
        sensors = settings.load_value_from_json_file("entities")
        if not sensors:
            return
        
        # Group entities by domain
        groups = {}
        for sensor in sensors:
            entity_id = sensor.get("entity_id", "")
            domain = entity_id.split('.')[0] if '.' in entity_id else 'other'
            if domain not in groups:
                groups[domain] = []
            groups[domain].append(sensor)
        
        # Create submenus based on configured threshold
        group_threshold = settings.load_value_from_json_file("group_threshold")
        if group_threshold is None:
            group_threshold = 5
        else:
            group_threshold = int(group_threshold)
        use_submenus = len(sensors) > group_threshold
        
        for domain, entities in sorted(groups.items()):
            if use_submenus and len(groups) > 1:
                # Create submenu for this domain
                submenu = QMenu(domain.capitalize(), menu)
                menu.addMenu(submenu)
                target_menu = submenu
            else:
                target_menu = menu
            
            for sensor in entities:
                entity_id = sensor.get("entity_id", "")
                friendly_name = sensor.get("friendly_name", entity_id)
                entity_type = sensor.get("type", "switch")
                entity_state = api.get_entity_state(entity_id)
                logger.info(f"Loaded sensor: {friendly_name} ({entity_id}) - {entity_type} - {entity_state}")
                
                if entity_type == "sensor":
                    action = QAction(f"{friendly_name} ({entity_state})", self)
                    action.setIcon(icons.get_icon('sensors_24dp_1976d2_fill0_wght400_grad0_opsz24'))
                    action.setToolTip(entity_id)
                    action.triggered.connect(lambda checked, s=sensor: self.on_sensor_selected(s))
                    target_menu.addAction(action)
                    
                elif entity_type == "switch":
                    action = QAction(f"{friendly_name} ({entity_state})", self)
                    if entity_state == "on":
                        action.setIcon(icons.get_icon('toggle_on_24dp_1976d2_fill0_wght400_grad0_opsz24'))
                    else:
                        action.setIcon(icons.get_icon('toggle_off_24dp_1976d2_fill0_wght400_grad0_opsz24'))
                    action.setToolTip(entity_id)
                    action.triggered.connect(lambda checked, s=sensor: self.on_switch_selected(s))
                    target_menu.addAction(action)

    def on_sensor_selected(self, sensor):
        if sensor:
            logger.info(f"Sensor selected: {sensor['friendly_name']} ({sensor['entity_id']})")

    def on_switch_selected(self, switch):
        if switch:
            current_state = api.get_entity_state(switch['entity_id'])
            new_state = "off" if current_state == "on" else "on"
            
            confirm_state_change = settings.load_value_from_json_file("confirm_state_change")
            if confirm_state_change:
                reply = QMessageBox.question(
                    self.parent,
                    "Confirm",
                    f"Toggle {switch['friendly_name']} from {current_state} to {new_state}?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    confirm_state_change = False

            if not confirm_state_change:
                success = api.set_entity_switch_state(switch['entity_id'], new_state)
                if success:
                    logger.info(f"Switch {switch['friendly_name']} ({switch['entity_id']}) set to {new_state.upper()}")
                else:
                    QMessageBox.critical(
                        self.parent,
                        "Error",
                        f"Failed to set {switch['friendly_name']} ({switch['entity_id']}) to {new_state.upper()}"
                    )
                    logger.info(f"Failed to set switch {switch['friendly_name']} ({switch['entity_id']}) to {new_state.upper()}")