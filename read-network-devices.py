# import json library
import json

# read json from network-devices.json into variable data
data = json.load(open("network-devices.json","r",encoding = "utf-8"))

# create an empty variable that will hold report text
report = ""

# include company name and date of last update in report
for name in data["company"]:
    report += name
for date in data["last_updated"]:
    report += date


# loop through location list
for location in data["locations"]:
    # include site name in report
    report += "\n" + location["site"] + "\n"
    # include device host names from each location in report
    for device in location["devices"]:
        report += " " + device["hostname"] + "\n"

# write data into a text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)