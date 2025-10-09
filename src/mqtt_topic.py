import logging
import subprocess
import json
import os
import wx
import yahac

logger = logging.getLogger(__name__)

def process_command(command, payload):
    """
    Handle a command received via MQTT.
    Args:
        command (str): The command name.
        payload (any): The associated value or parameters.
    """
    logger.info(f"Processing command: {command}, payload: {payload}")

    if not os.path.isfile(command):
        logger.error(f"[YAHAC] Topic command, error: Command not found: {command}")
        return

    if payload is None and ' ' in command:
        # split command into list for subprocess, if parameters are given in the command string
        command_parts = command.split(' ')
        command = command_parts[0]
        payload = command_parts[1:]
        
    # run the command as subprocess, but do not block the main thread
    if payload is None:
        subprocess.Popen([command])
    elif isinstance(payload, list):
        subprocess.Popen([command] + payload)
    else:
        subprocess.Popen([command, json.dumps(payload, default=str)])


def process_notification(payload):
    """
    Handle a notification received via MQTT.
    Args:
        payload (any): The notification data.
    """
    logger.info(f"Processing notification: {payload}")
    if os.name == "posix":
        subprocess.Popen(['notify-send', 'yahac', str(payload), '-t', '5000'])
    elif os.name == "nt":
        from win11toast import toast
        toast('yahac', str(payload), duration=5)
    else:
        logger.warning("Notifications are only supported on Linux (posix) and Windows (nt).")
