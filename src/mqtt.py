from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

import helper
import settings as yahac_settings

import paho.mqtt.client as mqtt
import threading

import json

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)


def create_mqtt_sensor(computername: str):
    # Configure the required parameters for the MQTT broker
    mqtt_host = yahac_settings.load_value_from_json_file("mqtt_host")
    mqtt_port = yahac_settings.load_value_from_json_file("mqtt_port")
    mqtt_user = yahac_settings.load_value_from_json_file("mqtt_user")
    mqtt_password = yahac_settings.load_value_from_json_file("mqtt_password")

    # Create MQTT settings
    try:
        mqtt_settings = Settings.MQTT(host=mqtt_host, port=mqtt_port, username=mqtt_user, password=mqtt_password)
    except Exception as e:
        raise Exception(f"Error creating MQTT settings: {e}")

    # Define the BinarySensorInfo
    sensor_info = BinarySensorInfo(
        name=f"yahac_{computername}",
        device_class="connectivity",
        unique_id=f"yahac_{computername}",
        state_topic=f"yahac/{computername}/state",
        availability_topic="yahac/availability",
        expire_after=10,
        state_stopped="off",
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
    yahac_sensor = BinarySensor(settings)

    # Add custom attributes
    yahac_sensor.set_attributes({
        "version": helper.VERSION,
        "website": helper.WEBSITE,
        "license": helper.LICENCE,
        "author": helper.AUTHOR
    })

    # Enable also a command listener
    def on_connect(client, userdata, flags, rc):
        logger.info(f"[MQTT] connected {rc}")
        topic = f"yahac/{computername}/command"
        client.subscribe(topic)
        logger.info(f"[MQTT] subscribed: {topic}")


    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        try:
            # receive the command like {"open_browser": "value"}
            data = json.loads(payload)
            logger.info(f"[MQTT] received command in JSON format: {data}")
            command = list(data.keys())[0]  # Get the first key as command
            payload = data[command]  # Get the associated value
            handle_command_json(command, payload)  # If you want to process the JSON object
        except json.JSONDecodeError:
            logger.warning(f"[MQTT] received command: {payload}. Handle as string.")
            handle_command(payload)

    def handle_command(command: str):
        if command == "run_script":
            logger.info("[YAHAC] command: run_script")
        else:
            logger.info(f"[YAHAC] Unsupported/unknown command: {command}")

    def handle_command_json(command: str, payload: dict):
        if command == "run_script":
            logger.info(f"[YAHAC] command: run_script, payload '{payload}'")
        else:
            logger.info(f"[YAHAC] Unsupported/unknown command: {command}")         

    # Start MQTT listener in background
    def start_mqtt_listener():
        client = mqtt.Client()
        client.username_pw_set(mqtt_user, mqtt_password)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(mqtt_host, int(mqtt_port), 60)
        client.loop_forever()

    listener_thread = threading.Thread(target=start_mqtt_listener, daemon=True)
    listener_thread.start()

    return yahac_sensor


def publish_sensor_state(sensor: BinarySensor, online: bool):
    state = "online" if online else "offline"
    sensor.update_state(state)
