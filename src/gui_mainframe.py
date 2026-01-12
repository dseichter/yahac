# Copyright (c) 2025-2026 Daniel Seichter
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

from PySide6.QtWidgets import QMainWindow, QMessageBox

import gui_traymenu
import gui_config
import settings
import icons as icons

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window with system tray integration."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YAHAC")
        self.resize(300, 200)
        self.move_to_center()
        self.hide()  # Start hidden, only tray icon visible
        
        # Set window icon
        self.setWindowIcon(icons.get_icon('home_app_logo_24dp_1976d2_fill0_wght400_grad0_opsz24'))
        
        self.tray_icon = gui_traymenu.TrayIcon(self)
        
        # Check if settings are available
        if not settings.CONFIGFILE:
            logger.warning("Configuration file not found. Creating default configuration.")
            settings.create_config()

        # Load configuration and check if url and token is set
        config = settings.read_config()
        if not config.get("url") or not config.get("token"):
            logger.warning("URL and token must be set in the configuration.")
            QMessageBox.warning(
                self,
                "Missing Configuration",
                "Please set the URL and token in the configuration."
            )
            config_dialog = gui_config.ConfigDialog(self)
            logger.info("Showing settings dialog")
            config_dialog.exec()

    def move_to_center(self):
        """Center the window on the screen"""
        screen_rect = self.screen().geometry()
        window_rect = self.frameGeometry()
        x = (screen_rect.width() - window_rect.width()) // 2
        y = (screen_rect.height() - window_rect.height()) // 2
        self.move(max(x, 0), max(y, 0))

    def closeEvent(self, event):
        """Handle window close event by minimizing to tray.
        
        Args:
            event: QCloseEvent
        """
        # Hide to tray instead of closing
        event.ignore()
        self.hide()
        if self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                "YAHAC",
                "Application was minimized to tray",
                icons.get_icon('home_app_logo_24dp_1976d2_fill0_wght400_grad0_opsz24'),
                2000
            )