import os
import sys
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
                               QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

import settings
import api
import icons as icons

if sys.platform.startswith("win"):
    import win32com.client

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(580, 500)
        self.setWindowIcon(icons.get_icon('settings_24dp_1976d2_fill0_wght400_grad0_opsz24'))
        
        self.token_visible = False
        self.setup_ui()
        self.load_settings()
        self.move_to_center()
    
    def move_to_center(self):
        """Center the dialog on the screen"""
        if self.parent():
            # Center relative to parent window
            parent_rect = self.parent().frameGeometry()
            dialog_rect = self.frameGeometry()
            x = parent_rect.x() + (parent_rect.width() - dialog_rect.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - dialog_rect.height()) // 2
            self.move(max(x, 0), max(y, 0))
        else:
            # Center on screen if no parent
            screen_rect = self.screen().geometry()
            dialog_rect = self.frameGeometry()
            x = (screen_rect.width() - dialog_rect.width()) // 2
            y = (screen_rect.height() - dialog_rect.height()) // 2
            self.move(x, y)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create grid layout for form fields
        grid = QGridLayout()
        
        # URL
        grid.addWidget(QLabel("URL:"), 0, 0)
        self.txt_url = QLineEdit()
        grid.addWidget(self.txt_url, 0, 1)
        
        # Token with show/hide button
        grid.addWidget(QLabel("Token:"), 1, 0)
        token_layout = QHBoxLayout()
        self.txt_token = QLineEdit()
        self.txt_token.setEchoMode(QLineEdit.Password)
        self.btn_show_token = QPushButton("Show")
        self.btn_show_token.setFixedWidth(60)
        self.btn_show_token.clicked.connect(self.on_show_token)
        token_layout.addWidget(self.txt_token)
        token_layout.addWidget(self.btn_show_token)
        grid.addLayout(token_layout, 1, 1)
        
        # Checkboxes
        self.chk_checkupdate = QCheckBox("Update on startup")
        grid.addWidget(self.chk_checkupdate, 2, 1)
        
        self.chk_autostart = QCheckBox("Autostart application")
        self.chk_autostart.stateChanged.connect(self.set_autostart)
        grid.addWidget(self.chk_autostart, 3, 1)
        
        self.chk_confirm_state_change = QCheckBox("Ask for confirmation before toggling switch")
        grid.addWidget(self.chk_confirm_state_change, 4, 1)
        
        self.chk_register_entity = QCheckBox("Register yahac as a Home Assistant entity using MQTT (restart required)")
        grid.addWidget(self.chk_register_entity, 5, 1)
        
        # MQTT settings
        grid.addWidget(QLabel("MQTT Host:"), 6, 0)
        self.txt_mqtt_host = QLineEdit()
        grid.addWidget(self.txt_mqtt_host, 6, 1)
        
        grid.addWidget(QLabel("MQTT Port:"), 7, 0)
        self.txt_mqtt_port = QLineEdit()
        grid.addWidget(self.txt_mqtt_port, 7, 1)
        
        grid.addWidget(QLabel("MQTT User:"), 8, 0)
        self.txt_mqtt_user = QLineEdit()
        grid.addWidget(self.txt_mqtt_user, 8, 1)
        
        grid.addWidget(QLabel("MQTT Password:"), 9, 0)
        self.txt_mqtt_password = QLineEdit()
        self.txt_mqtt_password.setEchoMode(QLineEdit.Password)
        grid.addWidget(self.txt_mqtt_password, 9, 1)
        
        # Log Level
        grid.addWidget(QLabel("Log Level:"), 10, 0)
        self.cmb_log_level = QComboBox()
        self.cmb_log_level.addItems(["DEBUG", "INFO", "ERROR"])
        grid.addWidget(self.cmb_log_level, 10, 1)
        
        layout.addLayout(grid)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_test = QPushButton("Test")
        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")
        
        self.btn_test.clicked.connect(self.on_test)
        self.btn_save.clicked.connect(self.on_save)
        self.btn_cancel.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_test)
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)
        
        layout.addLayout(button_layout)

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

        self.txt_url.setText(url if url else "")
        self.txt_token.setText(token if token else "")
        self.chk_checkupdate.setChecked(bool(checkupdate))
        self.chk_autostart.setChecked(bool(autostart))
        self.chk_confirm_state_change.setChecked(bool(confirm_state_change))
        self.chk_register_entity.setChecked(bool(register_entity))
        self.txt_mqtt_host.setText(mqtt_host if mqtt_host else "")
        self.txt_mqtt_port.setText(str(mqtt_port) if mqtt_port else "")
        self.txt_mqtt_user.setText(mqtt_user if mqtt_user else "")
        self.txt_mqtt_password.setText(mqtt_password if mqtt_password else "")
        self.cmb_log_level.setCurrentText(log_level if log_level else "INFO")

    def on_show_token(self):
        if self.token_visible:
            self.txt_token.setEchoMode(QLineEdit.Password)
            self.btn_show_token.setText("Show")
            self.token_visible = False
        else:
            self.txt_token.setEchoMode(QLineEdit.Normal)
            self.btn_show_token.setText("Hide")
            self.token_visible = True

    def on_test(self):
        url = self.txt_url.text()
        token = self.txt_token.text()
        if url and token:
            result = api.check_connection(url, token)
            QMessageBox.information(self, "Test", result)
        else:
            QMessageBox.warning(self, "Test", "Please provide both URL and Token.")

    def on_save(self):
        url = self.txt_url.text()
        token = self.txt_token.text()
        checkupdate = self.chk_checkupdate.isChecked()
        autostart = self.chk_autostart.isChecked()
        confirm_state_change = self.chk_confirm_state_change.isChecked()
        register_entity = self.chk_register_entity.isChecked()
        
        settings.save_config("url", url)
        settings.save_config("token", token)
        settings.save_config("checkupdate", checkupdate)
        settings.save_config("autostart", autostart)
        settings.save_config('confirm_state_change', confirm_state_change)
        settings.save_config('register_entity', register_entity)
        settings.save_config("mqtt_host", self.txt_mqtt_host.text())
        
        mqtt_port_text = self.txt_mqtt_port.text()
        mqtt_port = int(mqtt_port_text) if mqtt_port_text.isdigit() else 0
        settings.save_config("mqtt_port", mqtt_port)
        
        settings.save_config("mqtt_user", self.txt_mqtt_user.text())
        settings.save_config("mqtt_password", self.txt_mqtt_password.text())
        settings.save_config("loglevel", self.cmb_log_level.currentText())

        QMessageBox.information(self, "Save", "Settings saved.")
        self.accept()

    def set_autostart(self, state):
        autostart = state == Qt.Checked
        logger.info(f"Setting autostart to: {autostart}")
        app_name = "yahac"
        exe_path = sys.executable if getattr(sys, "frozen", False) else sys.argv[0]
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