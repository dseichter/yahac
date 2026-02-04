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
import socket
import json
import logging
from packaging import version

VERSION = "v0.4.2"
UPDATEURL = 'https://api.github.com/repos/dseichter/yahac/releases'
RELEASES = 'https://github.com/dseichter/yahac/releases'
WEBSITE = 'https://dseichter.github.io/yahac/'
NAME = 'yahac'
LICENCE = 'GPL-3.0'
AUTHOR = 'Daniel Seichter'


def check_for_new_release():
    """Check GitHub for newer stable releases.
    
    Returns:
        bool: True if newer version available, False otherwise
    """
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', UPDATEURL)
        releases = json.loads(r.data.decode('utf-8'))
        # Find the latest stable (not prerelease) release
        for release in releases:
            if not release.get('prerelease', False):
                latest_version = release.get('tag_name')
                return version.parse(latest_version) > version.parse(VERSION)
        return False  # No stable release found
    except Exception as e:
        logging.error(f"Error checking for new release: {e}")
        return False

def get_computer_name():
    """Get sanitized computer hostname.
    
    Returns:
        str: Lowercase alphanumeric hostname
    """
    hostname = socket.gethostname()
    # remove all non alphanumeric characters
    hostname = "".join(c for c in hostname if c.isalnum())
    # lowercase
    hostname = hostname.lower()
    return hostname