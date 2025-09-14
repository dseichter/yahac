import urllib3

import settings
import helper
import json

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)

http = urllib3.PoolManager()

settings.create_config()
URL = settings.load_value_from_json_file("url")
TOKEN = settings.load_value_from_json_file("token")

headers = {"Authorization": f"Bearer {TOKEN}", "User-Agent": f"{helper.NAME}/{helper.VERSION}"}


def check_connection(url, token):
    url = f"{url}/api/"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": f"{helper.NAME}/{helper.VERSION}"}
    try:
        response = http.request("GET", url, headers=headers)
        if response.status == 200:
            return "Your url and token are valid."
        else:
            return f"API returned status code: {response.status}"
    except Exception as e:
        return f"Error checking API status: {e}"


def check_api_status():
    url = f"{URL}/api/"
    try:
        response = http.request("GET", url, headers=headers)
        if response.status == 200:
            return "API is up and running"
        else:
            return f"API returned status code: {response.status}"
    except Exception as e:
        return f"Error checking API status: {e}"


def list_states():
    url = f"{URL}/api/states"
    try:
        response = http.request("GET", url, headers=headers)
        if response.status == 200:
            return json.loads(response.data.decode("utf-8"))
        else:
            return f"API returned status code: {response.status}"
    except Exception as e:
        return f"Error checking API status: {e}"


def get_entity_state(entity_id):
    url = f"{URL}/api/states/{entity_id}"
    try:
        response = http.request("GET", url, headers=headers)
        if response.status == 200:
            entitystate = json.loads(response.data.decode("utf-8"))
            current_state = entitystate.get("state", "unknown")
            unit_of_measurement = entitystate.get("attributes", {}).get("unit_of_measurement", "")
            return f"{current_state} {unit_of_measurement}".strip()
        else:
            return f"API returned status code: {response.status}"
    except Exception as e:
        return f"Error checking API status: {e}"


def set_entity_switch_state(entity_id, state):
    url = f"{URL}/api/services/switch/turn_{state}"
    payload = {"entity_id": entity_id}
    try:
        response = http.request("POST", url, headers=headers, body=json.dumps(payload))
        if response.status == 200:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error setting switch state: {e}")
        return False


def set_yahac_state(online: bool, computername: str):
    logger.info(f"Setting yahac sensor state to {'online' if online else 'offline'} for computer {computername}")
    url = f"{URL}/api/states/sensor.yahac_{computername}"
    state = 1 if online else 0
    payload = {
        "state": state,
        "attributes": {
            "type": "binary_sensor",
            "entity_id": f"yahac_{computername}",
            "is_on": True if online else False,
            "name": "yahac",
            "icon": "mdi:access-point-network",
            "attribution": "Data provided by yahac",
            "source": "yahac",
            "version": helper.VERSION,
            "website": helper.WEBSITE,
            "license": helper.LICENCE,
            "author": "Daniel Seichter",
            "device_class": "BinarySensorDeviceClass.CONNECTIVITY",
            "state_class": "measurement",
            "next_update": "manual"
        },
    }
    try:
        response = http.request("POST", url, headers=headers, body=json.dumps(payload))
        if response.status == 200:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error setting yahac sensor state: {e}")
        return False


def remove_yahac_entity(computername: str):
    logger.info("Removing yahac entity from Home Assistant")
    url = f"{URL}/api/states/sensor.yahac_{computername}"
    try:
        response = http.request("DELETE", url, headers=headers)
        if response.status == 200:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error removing yahac entity: {e}")
        return False
