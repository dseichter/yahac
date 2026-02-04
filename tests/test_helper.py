import os
import sys
import json
from unittest.mock import MagicMock, patch

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import helper


def test_get_computer_name_contains_only_alnum_and_lowercase():
    """Test computer name is lowercase and alphanumeric."""
    name = helper.get_computer_name()
    assert name == name.lower()
    assert name.isalnum()


def test_check_for_new_release_ignores_prereleases_and_detects_new():
    """Test release check ignores prereleases and detects newer versions."""
    # releases list contains a prerelease first, then a stable
    releases = [
        {"tag_name": "v0.4.0-beta", "prerelease": True},
        {"tag_name": "v0.4.0", "prerelease": False},
    ]

    mock_response = MagicMock()
    mock_response.data = json.dumps(releases).encode('utf-8')

    mock_pm = MagicMock()
    mock_pm.request.return_value = mock_response

    with patch('helper.urllib3.PoolManager', return_value=mock_pm):
        # pretend current VERSION is older than v0.4.0
        with patch.object(helper, 'VERSION', 'v0.3.0'):
            assert helper.check_for_new_release() is True


def test_check_for_new_release_no_stable_found_returns_false():
    """Test release check returns False when no stable releases exist."""
    releases = [
        {"tag_name": "v0.5.0-rc1", "prerelease": True},
        {"tag_name": "v0.6.0-alpha", "prerelease": True},
    ]

    mock_response = MagicMock()
    mock_response.data = json.dumps(releases).encode('utf-8')

    mock_pm = MagicMock()
    mock_pm.request.return_value = mock_response

    with patch('helper.urllib3.PoolManager', return_value=mock_pm):
        with patch.object(helper, 'VERSION', 'v0.3.0'):
            assert helper.check_for_new_release() is False
