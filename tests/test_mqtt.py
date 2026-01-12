import os
import sys

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import mqtt


class DummySensor:
    """Mock sensor for testing MQTT state updates."""
    def __init__(self):
        self.last_state = None

    def update_state(self, state):
        """Simulate sensor state update.
        
        Args:
            state: Sensor state string
        """
        # simulate the ha sensor's update_state method
        self.last_state = state


def test_publish_sensor_state_online_offline():
    """Test sensor state transitions between online and offline."""
    s = DummySensor()
    mqtt.publish_sensor_state(s, True)
    assert s.last_state == 'online'
    mqtt.publish_sensor_state(s, False)
    assert s.last_state == 'offline'
