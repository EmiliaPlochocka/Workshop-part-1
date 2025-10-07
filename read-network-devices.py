# import json library
import json

# read json from network-devices.json into variable data
data = json.load(open("network-devices.json","r",encoding = "utf-8"))

# create an empty variable that will hold report text
report = ""

# ___HEADER___
# create an empty header
header = ""
header += "Networking report for:\n"
# include company name and date of last update in header
for name in data["company"]:
    header += name
header += "\n"
for date in data["last_updated"]:
    header += date
header += "\n"
# add header before main report
report = header + report

#___LOW UPTIME___
# loop through devices with uptime of less than 30 days
report += "\n" + "Devices with less than 30 days of uptime:\n"
for location in data["locations"]:
    # include site name in report
    report += "\n" + location["site"] + "\n"
    # include devices in report
    for device in location["devices"]:
        if device["uptime_days"] <30:
            report += (" "
                     + device["hostname"].ljust(15,' ') + ' '
                     + "Uptime days:".ljust(15) + ' '
                     + str(device["uptime_days"]).rjust(4) + "\n"
                     )

#___STATUS___
# loop through devices with offline or warning status
report += "\n" + "Devices with 'offline' or 'warning' status:\n"
for location in data["locations"]:
    for device in location["devices"]:
        if device["status"] == "offline" or device["status"] == "warning":
            report += "\n" + location["site"] + "\n"
            report += (" "
                     + device["hostname"].ljust(15,' ') + ' '
                     + (device["status"]).rjust(4) + "\n"
                     )
#___COUNT DEVICES___
# create new dictionary and add start values
counts = {}
counts = {'switch': 0, 'router': 0, 'access_point': 0, 'firewall': 0, 'load_balancer': 0}
for location in data["locations"]:
    for device in location["devices"]:
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

# fetch value
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


#___write data into a text file___
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)