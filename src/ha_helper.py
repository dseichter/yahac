import api

import socket

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)


def set_entity_state_online():
    logger.info("Change yahac state to online.")
    # trigger rest api call to get the current state
    api.set_yahac_state(True, get_computer_name())


def set_entity_state_offline():
    logger.info("Change yahac state to offline.")
    # trigger rest api call to get the current state
    api.set_yahac_state(False, get_computer_name())


def get_computer_name():
    hostname = socket.gethostname()
    # remove all non alphanumeric characters
    hostname = "".join(c for c in hostname if c.isalnum())
    # lowercase
    hostname = hostname.lower()
    return hostname
