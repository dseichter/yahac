# Automation

Each yahac client can be integrated into the Homa Assistants' Automation. 

If you have enabled MQTT, yahac automatically subscribes to the topic `yahac/<computername>/command`.

Replace the computername with your yahac client and adjust your payload.

## Example

This example automation will run test_mqtt_script.sh, located within my home directory, after the client is connected (startup of the yahac client).

```YAML
alias: yahac Test
description: ""
triggers:
  - type: connected
    device_id: 908faa2294da1c3e0c063a366d08de8f
    entity_id: e4635fbad32b512e3c84d9f0f12a53c6
    domain: binary_sensor
    trigger: device
conditions: []
actions:
  - action: mqtt.publish
    metadata: {}
    data:
      evaluate_payload: false
      qos: "2"
      retain: false
      topic: yahac/<computername>/command
      payload: "{\"run_script\": \"~/test_mqtt_script.sh\"}"
mode: single
```

You can provide any script you want to run on each yahac client. If your provided script should only run once, take care about QOS.

## Supported commands

### run_script

This command will run the provided script/executable.

Further commands I will add, if there is the need. 