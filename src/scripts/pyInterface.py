import os
import sys
import logging
import json
import time
import census2xlsx
import xlsxwriter

log_dir = "./logs"

report_area = json.loads(sys.argv[1])
selected_indicators = json.loads(sys.argv[2])
options = json.loads(sys.argv[3])

c2x = census2xlsx.Census2Xlsx(options["dataDir"], log_dir)

# create tmp variables for storing census tables and custom tables
census_tables = {}
custom_tables = {}

# sort report_area by geographic level and then primary ID
report_area = sorted(
    report_area,
    key=lambda location: (location["geographicLevel"]),
    reverse=True,
)
report_area = sorted(report_area, key=lambda location: (location["primaryID"]))

sys.stdout.flush()

# for each table in selected_tables, add table indicators to list to be downloaded
c2x.select_tables(selected_indicators)

# for each location in report_area, download the census data and store in census_tables
for i in range(len(report_area)):
    location_name = report_area[i]["locationName"]
    print(f"Downloading {location_name} data... {round((i / len(report_area)), 2)}")
    sys.stdout.flush()
    c2x.download_tables(report_area[i], census_tables)

print("Calculating indicators... 1")
sys.stdout.flush()

# calculated the selected tables and store in custom_tables
# tmp is used for calculating custom_tables. It is removed at end of calculations
custom_tables["tmp"] = ""
c2x.calculate_tables(selected_indicators, census_tables, custom_tables)
del custom_tables["tmp"]

# TODO: use or remove:
# print(json.dumps(custom_tables, indent=4))

time.sleep(0.5)
print("Saving indicators... 1")
sys.stdout.flush()

# save custom_tables to .xlsx file defined by output_path
workbook = xlsxwriter.Workbook(options["outputFile"])
c2x.save_tables(workbook, census_tables, custom_tables)
workbook.close()

time.sleep(0.5)
print("1.01")