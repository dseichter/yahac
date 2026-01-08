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

import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

import gui_mainframe
import settings
import helper
import mqtt
import webbrowser
import threading

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)


class YahacApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)
        
        settings.create_config()
        
        # Check for update if enabled
        if settings.load_value_from_json_file("checkupdate"):
            if helper.check_for_new_release():
                reply = QMessageBox.question(
                    None,
                    "Update available",
                    "A new release is available.\nWould you like to open the download page?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    webbrowser.open_new_tab(helper.RELEASES)

        self.main_window = gui_mainframe.MainWindow()
        
        if settings.load_value_from_json_file("register_entity"):
            logger.info("Get (or create) MQTT sensor.")
            try:
                self.ha_helper = mqtt.create_mqtt_sensor(helper.get_computer_name())
                logger.info("Create timer and set entity state online.")
                self.timer = QTimer()
                self.timer.timeout.connect(self.on_timer)
                self.timer.start(5000)  # Check every 5 seconds
            except Exception as e:
                QMessageBox.critical(
                    None,
                    "MQTT Error",
                    f"Are your MQTT settings correct? Please check your configuration.\n\n{e}"
                )

    def on_timer(self):
        # Run MQTT publish in a separate thread to avoid blocking the GUI
        thread = threading.Thread(target=mqtt.publish_sensor_state, args=(self.ha_helper, True), daemon=True)
        thread.start()


def main():
    """Main entry point for the application."""
    app = YahacApp(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()