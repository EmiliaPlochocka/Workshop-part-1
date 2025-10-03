# import json library
import json

# read json from network-devices.json into variable devices
devices = json.load(open("network-devices.json","r",encoding = "utf-8"))

print(devices)