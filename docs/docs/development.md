# Development

## Start development

I am using pyenv on my computers and virtual machines.

Create and activate an environment by running the following command:

```pyenv virtualenv 3.13.7 yahac-venv```

```pyenv activate yahac-venv```

Install the required dependencies

```pip install -r src/requirements.txt```
```pip install -r icons/requirements.txt```
```pip install -r docs/requirements.txt```

You can start the yahac by running the following command:

```cd src && python yahac.py```

## Testing

At this time, there is no automated test available. The following test steps are done on **all** Windows and Linux distributions:

* Delete old configuration to have a fresh setup
* Run yahac binary
* Message should appear to request for configuration
* Provide information (URL and token)
* Restart application
* Message regarding configuration should not appear anymore
* Open Sensors
* Add first entity with type sensor (a dynamic one, so check if new values are reported)
* Add second entity with type switch (change to switch).
* Save
* Sensor and switch should be shown in Tray Menu
* State (current value) of sensor should change while opening the tray menu.
* Trigger switch to change state
* Entity of type switch should now change it's state
* Click on "Check for update" (no update should be shown, except there was meanwhile a new release)
* Click on "Open Documentation" and a browser should open and browse to [yahac documentation](https://dseichter.github.io/yahac/)


## Resources

### Images

If you add further images, taken from [Google Material Symbols](https://fonts.google.com/icons), please add this to table below within your PR.

#### Overview Icon usage

Base color: #1976D2

Alphabetical order:

| Image name                                               | Usage |
| -------------------------------------------------------- | ----- |
| database_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png      | Sensors frame (add/remove sensors) |
| globe_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png         | link to website |
| home_app_logo_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png | YAHAC itself, ICO file available |
| logout_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png        | TrayMenu Exit |
| sensors_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png       | Listed sensor in Traymenu |
| settings_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png      | Configuration frame (settings) |
| toggle_off_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png    | TrayMenu switch with state off |
| toggle_on_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png     | TrayMenu switch with state on |
| update_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png        | TrayMenu Check for updates |

If more icons are are being added, list them. Keep original filename for faster identification.