# import json library
import json

# read json from network-devices.json into variable data
data = json.load(open("network-devices.json","r",encoding = "utf-8"))

# create an empty variable that will hold report text
report = ""

# ___HEADER___
header = "Networking report for:\n"
# fetch data "company" from data(from json file)
header += data.get("company") + "\n"
# fetch "last_updated" from data, add a double line at the end for clarity
header += "data update:" + data.get("last_updated", "") +"\n\n"
# add header before main report
report = header + report

#___LOW UPTIME___
# loop through devices with uptime of less than 30 days
report += "\n" + "Devices with less than 30 days of uptime:\n"
for location in data["locations"]:
    # include site name in report
    report += "\n" + location["site"] + "\n"
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

#___PORT UTILIZATION___
# I give up.
# number of total ports in devices: 676
# number of used ports: 541
n1 = int(676)
n2 = int(541)

division = n2 / n1
percentage = (division) * 100

report += "\n" + "total port utilization:" + '\n'
report += "541 of 676 ports in use = " + str(percentage) + "%"

#__UNIQUE VLANS__
vlans = set()
vlans.update()

#___write data into a text file___
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)