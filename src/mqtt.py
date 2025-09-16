from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

import helper
import settings as yahac_settings


def create_mqtt_sensor(computername: str):
    # Configure the required parameters for the MQTT broker
    mqtt_host = yahac_settings.load_value_from_json_file("mqtt_host")
    mqtt_port = yahac_settings.load_value_from_json_file("mqtt_port")
    mqtt_user = yahac_settings.load_value_from_json_file("mqtt_user")
    mqtt_password = yahac_settings.load_value_from_json_file("mqtt_password")

    # Create MQTT settings, but if any parameter is missing, raise an exception
    try:
        mqtt_settings = Settings.MQTT(host=mqtt_host, port=mqtt_port, username=mqtt_user, password=mqtt_password)
    except Exception as e:
        raise Exception(f"Error creating MQTT settings: {e}")

    # Information about the sensor
    sensor_info = BinarySensorInfo(
        name=f"yahac_{computername}",
        device_class="connectivity",
        unique_id=f"yahac_{computername}",
        state_topic=f"yahac/{computername}/state",
        availability_topic="yahac/availability",
        payload_on="online",
        payload_off="offline",
        expire_after=10,  # double the timer interval to mark the sensor as unavailable
        state_stopped="offline",
        retain=True,
        device={
            "identifiers": ["yahac"],
            "name": "YAHAC",
            "model": "Yet Another Home Assistant Client",
            "manufacturer": "Daniel Seichter",
        },
    )

    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

    # Instantiate the sensor
    mysensor = BinarySensor(settings)

    # You can also set custom attributes on the sensor via a Python dict
    mysensor.set_attributes({"version": helper.VERSION, "website": helper.WEBSITE, "license": helper.LICENCE, "author": helper.AUTHOR})
    return mysensor


def publish_sensor_state(sensor: BinarySensor, online: bool):
    state = "online" if online else "offline"
    sensor.update_state(state)
