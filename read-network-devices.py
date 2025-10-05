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
        if device["uptime_days"] <30:
            report += (" "
                     + device["hostname"].ljust(15,' ') + ' '
                     + device["status"].ljust(15) + ' '
                     + str(device["uptime_days"]).rjust(4) + "\n"
                     )

# create an empty summary
summary = ""
summary += "Summary:\n"
summary += "This is our basic report:\n"
    
# add summary before main report
report = summary + report


# write data into a text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)