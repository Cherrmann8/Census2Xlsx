"""
File: testDownloadSpeed.py
Brief: A script for testing the censusdata library.
Details: Test the download method from the censusdata library to see what gives the best performance.

Author: Charles Herrmann
Date: 10/5/20
"""

import sys
import getopt
import json
import time
import censusdata

# Global Variables
censusType = "acs5"
censusYear = 2019
dataDir = "./src/assets/data/"


def downloadData():
    indicatorCodes = {}
    tmpGeoCode = censusdata.censusgeo([("state", "01"), ("county", "001")])

    # load censusTables.json
    with open(dataDir + "censusTables.json", "r") as loadfile:
        censusTablesFile = json.load(loadfile)

    # add all indicators to a dictionary of lists
    for section in censusTablesFile:
        indicatorCodes[section] = []
        for table in censusTablesFile[section]:
            for indicator in censusTablesFile[section][table]:
                indicatorCodes[section].append(indicator)

    # start the test
    print("Starting the All At Once test...")
    start = time.perf_counter()
    censusdata.download(
        censusType,
        censusYear,
        tmpGeoCode,
        indicatorCodes["Detailed Tables"],
        tabletype="detail",
    )
    stop = time.perf_counter()
    print(f"Downloading all at once took {(stop-start):0.3f} seconds.")

    print("Starting the One At A Time test...")
    total = 0
    for indicator in indicatorCodes["Detailed Tables"]:
        start = time.perf_counter()
        censusdata.download(
            censusType,
            censusYear,
            tmpGeoCode,
            [indicator],
            tabletype="detail",
        )
        stop = time.perf_counter()
        total += stop - start
    count = len(indicatorCodes["Detailed Tables"])
    avg = total / count
    print(f"Downloading all at once took {total:0.3f} seconds.")
    print(f"An average of {avg:0.3f} seconds for the {count} indicators.")


def usage():
    print("Usage: testDownloadSpeed.py")


def main():
    downloadData()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        usage()
    else:
        main()