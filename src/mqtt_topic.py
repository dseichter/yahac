import logging
import subprocess # nosec B404
import json
import os
import settings

logger = logging.getLogger(__name__)

def process_command(command, payload, secstring):
    """
    Handle a command received via MQTT.
    Args:
        command (str): The command name.
        payload (any): The associated value or parameters.
    """
    logger.info(f"Processing command: {command}, payload: {payload}")

    # check, if securestring is used (enabled) and it is included in payload
    securestring_use = bool(settings.load_value_from_json_file("securestring_use"))
    securestring = settings.load_value_from_json_file("securestring")

    if securestring_use and securestring:
        if securestring == secstring or securestring in str(command):
            logger.info("Securestring is correct, executing command.")
        else:
            logger.warning("Securestring is incorrect, command not executed.")
            return

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
            subprocess.Popen([command])  # nosec B603
        elif isinstance(payload, list):
            subprocess.Popen([command] + payload)  # nosec B603
        else:
            subprocess.Popen([command, json.dumps(payload, default=str)])  # nosec B603
        return

    # Unknown command
    logger.warning(f"Unknown command: {command}")


def process_notification(payload, secstring):
    """
    Handle a notification received via MQTT.
    Args:
        payload (any): The notification data.
    """
    logger.info(f"Processing notification: {payload}")

    # check, if securestring is used (enabled) and it is included in payload
    securestring_use = bool(settings.load_value_from_json_file("securestring_use"))
    securestring = settings.load_value_from_json_file("securestring")

    if securestring_use and securestring:
        if securestring == secstring:
            logger.info("Securestring is correct, executing command.")
        else:
            logger.warning("Securestring is incorrect, command not executed.")
            return

    # be able to show JSON payloads nicely formatted
    try:
        payload = json.dumps(payload, default=str, indent=2)
    except (TypeError, ValueError):
        payload = payload

    if os.name == "posix":
        subprocess.Popen(['notify-send', 'yahac', str(payload), '-t', '5000'])  # nosec B603 B607
    elif os.name == "nt":
        from win11toast import toast
        toast('yahac', str(payload), duration=5)
    else:
        logger.warning("Notifications are only supported on Linux (posix) and Windows (nt).")
