from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

import helper
import settings as yahac_settings
import mqtt_topic

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
    except (ValueError, TypeError, ConnectionError) as e:
        raise RuntimeError(f"Error creating MQTT settings: {e}") from e

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
        topics = [
            f"yahac/{computername}/command",
            f"yahac/{computername}/notify"
        ]
        for topic in topics:
            client.subscribe(topic)
            logger.info(f"[MQTT] subscribed: {topic}")


    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        topic = msg.topic
        try:
            data = json.loads(payload)
            logger.info(f"[MQTT] received JSON on topic '{topic}': {data}")
            handle_command_json(topic, data)
        except json.JSONDecodeError:
            logger.info(f"[MQTT] received string on topic '{topic}': {payload}")
            handle_command_string(topic, payload)


    def handle_command_json(topic: str, payload: dict):
        if topic.endswith("/command"):
            command = payload.get("command")
            securestring = payload.get("securestring")
            data = payload.get("data") # default is None, therefore, no additional parameters
            logger.info(f"[YAHAC] topic 'command': {command}, data: {data}")
            mqtt_topic.process_command(command, data, securestring)
        elif topic.endswith("/notify"):
            content = payload.get("message")
            securestring = payload.get("securestring")
            logger.info(f"[YAHAC] topic 'notify': {content}")
            mqtt_topic.process_notification(content, securestring)
        else:
            logger.warning(f"[YAHAC] Unknown/unhandled topic: {topic}")

    def handle_command_string(topic: str, payload: str):
        if topic.endswith("/command"):
            # read --securestring=<value>, if available and extract it
            command = payload.split("--securestring=")[0].strip()
            securestring = None
            if len(payload.split("--securestring=")) > 1:
                securestring = payload.split("--securestring=")[1].strip()
            logger.info(f"[YAHAC] topic 'command': {command}")
            mqtt_topic.process_command(command, None, securestring)
        elif topic.endswith("/notify"):
            content = payload.split("--securestring=")[0].strip()
            securestring = None
            if len(payload.split("--securestring=")) > 1:
                securestring = payload.split("--securestring=")[1].strip()
            logger.info(f"[YAHAC] topic 'notify': {content}")
            mqtt_topic.process_notification(content, securestring)
        else:
            logger.warning(f"[YAHAC] Unknown/unhandled topic: {topic}")
      

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
