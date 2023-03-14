#!/usr/bin/env python3

import json

example_config = {  
  "global":
        { "read_interval_seconds" : 30
        },        
  "mqtt":
        { 
          "broker" : "192.168.1.2",
          "port" : 1883,
          "keepalive" : 60,
          "topic_root" : "raspi"
        }
}


# write json file
output_json = 'config.example.json'
with open(output_json, 'w') as jsonfile:
    print('saving to', output_json)
    json.dump(example_config, jsonfile, indent=2)