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
    """Check Home Assistant API connection with provided credentials.
    
    Args:
        url: Home Assistant URL
        token: Authentication token
        
    Returns:
        str: Status message
    """
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
    """Check if Home Assistant API is accessible.
    
    Returns:
        str: API status message
    """
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
    """Retrieve all entity states from Home Assistant.
    
    Returns:
        list: Entity states or error message
    """
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
    """Get current state of a specific entity.
    
    Args:
        entity_id: Entity identifier
        
    Returns:
        str: Entity state with unit or error message
    """
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
    """Toggle switch entity state.
    
    Args:
        entity_id: Entity identifier
        state: Target state ('on' or 'off')
        
    Returns:
        bool: True if successful, False otherwise
    """
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
