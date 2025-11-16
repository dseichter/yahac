import logging
import subprocess
import json
import os

logger = logging.getLogger(__name__)

def process_command(command, payload):
    """
    Handle a command received via MQTT.
    Args:
        command (str): The command name.
        payload (any): The associated value or parameters.
    """
    logger.info(f"Processing command: {command}, payload: {payload}")

    # First, handle known logical commands
    if command == "run_script":
        logger.info(f"Running script with payload: {payload}")
        # Implement script execution here if desired
        return
    if command == "message_box":
        logger.info(f"Showing message box: {payload}")
        # Integrate with GUI to show message boxes if needed
        return

    # If the command looks like an executable path, try to run it
    if os.path.isfile(command):
        # If payload is None and command contains parameters, split them
        if payload is None and ' ' in command:
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
        return

    # Unknown command
    logger.warning(f"Unknown command: {command}")


def process_notification(payload):
    """
    Handle a notification received via MQTT.
    Args:
        payload (any): The notification data.
    """
    logger.info(f"Processing notification: {payload}")

    # be able to show JSON payloads nicely formatted
    try:
        payload = json.dumps(payload, default=str, indent=2)
    except (TypeError, ValueError):
        payload = payload

    if os.name == "posix":
        subprocess.Popen(['notify-send', 'yahac', str(payload), '-t', '5000'])
    elif os.name == "nt":
        from win11toast import toast
        toast('yahac', str(payload), duration=5)
    else:
        logger.warning("Notifications are only supported on Linux (posix) and Windows (nt).")
