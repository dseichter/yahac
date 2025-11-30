#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="yahac",
    version="0.4.1",
    description="Yet Another Home Assistant Client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniel Seichter",
    author_email="daniel.seichter@dseichter.de",
    url="https://github.com/dseichter/yahac",
    license="GPL-3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "PySide6>=6.10.1",
        "urllib3>=2.5.0",
        "paho-mqtt>=2.1.0",
        "pywin32>=311; sys_platform == 'win32'",
        "win11toast>=0.36.2; sys_platform == 'win32'",
        "ha_mqtt_discoverable>=0.23.0",
    ],
    entry_points={
        "console_scripts": [
            "yahac=yahac:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Home Automation",
        "Topic :: Desktop Environment",
    ],
)