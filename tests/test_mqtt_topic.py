import os
import sys
import logging

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import mqtt_topic


def test_process_command_run_script_logs(caplog):
    caplog.set_level(logging.INFO)
    mqtt_topic.process_command('run_script', {'path': '/tmp/test.sh'})
    assert any('Running script' in r.message for r in caplog.records)


def test_process_command_unknown_logs(caplog):
    caplog.set_level(logging.WARNING)
    mqtt_topic.process_command('unknown_cmd', None)
    assert any('Unknown command' in r.message or 'Unknown command' in r.getMessage() for r in caplog.records)


def test_process_notification_logs(caplog):
    caplog.set_level(logging.INFO)
    mqtt_topic.process_notification('Hello world')
    assert any('Processing notification' in r.message for r in caplog.records)
