# yahac - Yet Another Home Assistant Client

yahac - Yet Another Home Assistant Client - is a tool to show your most important entities of Home Assistant.
See current values/states of your sensors or turn on/off your switches. And everything in the tray area.

![yahac in tray Icon](assets/screenshots/yahac_traymenu_with_entities.png)

You can configure as much as needed sensors and switches. As soon as you show the menu (right click on the yahac icon), the latest value of your entities will be collected and shown.

A full list of compatible and tested operating systems, can be found in the [compatibility](compatibility.md) overview.

## Start yahac

You won't see any window appear, because yahac starts only as tray icon in your task bar. Follow the [installation instruction](installation.md) if you start yahac the first time.

### Check for updates

Next to the list of your entities, you will find the possibility to check for updates.

### Open Documentation

This will open this documentation.

## Known issues

### Windows Defender 
There is a false positive alert after downloading the windows binary [#34](https://github.com/dseichter/yahac/issues/34). Exclude this file from your Windows Defender. I am working on it.

### GNOME
GNOME does not support Tray Menu out of the box. There are serveral solutions to enable a tray menu within GNOME. I can't recommend any of them at the moment.