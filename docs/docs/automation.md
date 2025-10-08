# Automation

Each yahac client can be integrated into automation. It subscsribes automatically to the topic 'yahac/computername/command'.

An example automation can look like

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
      topic: yahac/daniellinuxmint/command
      payload: "{\"run_script\": \"~/test_mqtt_script.sh\"}"
mode: single
```

You can provide any script you want to run on each yahac client.