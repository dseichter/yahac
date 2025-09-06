# Sensor

You can add a lot of sensors and switches to yahac. The number is not limited.

## Add entities

If you open the sensors window of yahac the first time, you will see an empty windows.

![Sensors - first start](assets/screenshots/yahac_sensors_empty.png)

Open the combobox (drop down list) which will represent you all possible entities within your Home Assistant instance.
This list contains the entity_ids, which are unique.

![Sensors - select entity](assets/screenshots/yahac_sensors_select_entity.png)

After you have selected the entry from the combobox, it will automatically being added to the list of entities. You will also see the "Friendly name" (the one, you have configuration within HA) and the type. Per default, the type is `sensor`.

![Sensors - add entity sensor](assets/screenshots/yahac_sensors_add_entity_sensor.png)

### Switches
If you want to add a switch, you have after your selection of the entity to change the type. Just click on the entry and a list of possible types will be present. Choose `switch`

![Sensors - add entity switch](assets/screenshots/yahac_sensors_add_entity_switch.png)

### Save your entities
Now, it's time to save your choosen entities. There is **no autosave**, so please do not forget.

![Sensors - save](assets/screenshots/yahac_sensors_save.png)

After you have choosen your sensors, they will appear immediately in the menu of yahac.

![yahac in tray Icon](assets/screenshots/yahac_traymenu_with_entities.png)