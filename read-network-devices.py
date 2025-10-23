# import json library
import json

# read json from network-devices.json into "data"
data = json.load(open("network-devices.json","r",encoding = "utf-8"))

# create an empty variable that will hold report text
report = ""


# ___HEADER___
header = "Networking report for:\n"
# Fetch name of company from JSON
# data.get("company") gets the key "company" from dictionary "data"
# can also be written as: data["company"], but can output an error if key "company" is not present

header += data.get("company") + "\n"
# fetch last updated timestamp from JSON
# add double line at the end for structure

header += "data update:" + data.get("last_updated", "") +"\n\n"
# add header before main report
report = header + report


#___LOW UPTIME___
report += "\n" + "Devices with less than 30 days of uptime:\n"
# loop through locations in "data"
# insert an empty space[] if the key "locations" is not present

for location in data.get("locations", []):
    # f" - formatted string literal
    # f" enables variables to be inserted{} directly into a string
    # you can also write as: report += \n + (location.get('site)) + \n
    report += f"\n{location.get('site')}\n"

    # loop through device in location
    for device in location.get("devices", []):
        # fetch uptime days
        uptime = device.get("uptime_days")

        # if uptime days are greater than 30
        try:
            if uptime is not None and int(uptime) <30:
                report += (
                    " " + device.get("hostname", "").ljust(15) + " "
                    + "Uptime days:".ljust(15) + " "
                    + str(int(uptime)).rjust(4) + "\n"
                     )
                
        # if key "uptime_days" is empty, skip
        except (ValueError, TypeError):
            continue


#___WARNING/OFFLINE STATUS___
report += "\nDevices with 'offline' or 'warning' status:\n"

# loop through location in data
for location in data.get("locations", []):

    site = location.get("site")
    # create a list with only the status "offline" or "warning"
    problems = [d for d in location.get("devices", [])
            if d.get("status") in ("offline", "warning")
            ]
    
    # if devices with other status are presen, ignore
    if not problems:
        continue

    # add site name
    report += f"\n{site}\n"

    # loop through devices and display status
    for device in problems:
            status = device.get("status", "")
            report += (
                " " + device.get("hostname", "").ljust(15) + " "
                 + status.ljust(7) + "\n"
            )


#___COUNT DEVICES___
# create new dictionary and add start values
counts = {}
counts = {'switch': 0, 
          'router': 0, 
          'access_point': 0, 
          'firewall': 0, 
          'load_balancer': 0}

for location in data["locations"]:
    for device in location["devices"]:

        # add to counter of corresponding device type
        if device["type"] == "switch":
            counts['switch'] += 1
        if device["type"] == "router":
            counts['router'] += 1
        if device["type"] == "access_point":
            counts['access_point'] += 1
        if device["type"] == "firewall":
            counts['firewall'] += 1
        if device["type"] == "load_balancer":
            counts['load_balancer'] += 1

# convert values into text variables
count_switch = counts["switch"]
count_router = counts["router"]
count_access_point = counts["access_point"]
count_firewall = counts["firewall"]
count_load_balancer = counts["load_balancer"]

# add sum of devices to report
report += "\n" + "List of all devices by type:\n"
report += "\n" + "number of switches:" + " " + str(count_switch) + "\n"
report += "number of routers:" + " " + str(count_router) + "\n"
report += "number of switcaccess points:" + " " + str(count_access_point) + "\n"
report += "number of firewalls:" + " " + str(count_firewall) + "\n"
report += "number of load balancers:" + " " + str(count_load_balancer) + "\n"


#___PORT UTILIZATION___
total_ports = 0
used_ports = 0

# loop through devices in locations
for loc in data.get("locations", []):
    for dev in loc.get("devices", []):
        ports = dev.get("ports")

        # isinstance = if "ports" is an existing key and is a dictionary (dict)
        if ports and isinstance(ports, dict):
            try:
                total = int(ports.get("total", 0))
                used = int(ports.get("used", 0))
            except (ValueError, TypeError):
                total = 0
                used = 0
            
            # sum the number of ports
            total_ports += total
            used_ports += used

# calculate the percentage of used ports per total ports
if total_ports > 0:
    percentage = used_ports / total_ports * 100
else:
    percentage = 0.0

# f"{percentage:.1f}":
# f" = format float; percentage = value of (used/ total ports * 100);
# :.1f = round up to one decimal space, format value as float
report += "\nTotal port utilization:\n"
report += f"{used_ports} of {total_ports} ports in use = {percentage:.1f}%\n"


#__UNIQUE VLANS__
# set() - elliminate duplicate values
vlans = set()

for loc in data.get("locations", []):
    for dev in loc.get("devices", []):
        for v in dev.get("vlans", []):
            try:
                # add VLAN as an integer/number
                vlans.add(int(v))
            except (ValueError, TypeError):
                continue

# sort VLANS, ascending
sorted_vlans = sorted(vlans)

report += "\nUnique VLANs in network:\n"
if sorted_vlans:
    # .join adds commas "," between each output
    report += ", ".join(str(v) for v in sorted_vlans) + "/n"
else:
    report += "None found\n"


#___OVERVIEW PER LOCATION___
report += "\nOverview per location:\n"

for loc in data.get("locations", []):
    site_name = loc.get("site", "Unknown site")

    # len - calculates the number of elements in the object (devices)
    total_devices = len(loc.get("devices", []))
    # counters for each status
    online_count = 0
    offline_count = 0
    warning_count = 0

    # count status of each device in locations
    for dev in loc.get("devices", []):
        status = dev.get("status", "").lower()
        if status == "online":
            online_count += 1
        elif status == "offline":
            offline_count += 1
        elif status == "warning":
            warning_count += 1

    # add results to raport
    report += f"\n{site_name}\n"
    report += f" Total devices: {total_devices}\n"
    report += f" Online: {online_count}\n"
    report += f" Offline: {offline_count}\n"
    report += f" Warning: {warning_count}\n"

#___WRITE TEXT FILE___
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)