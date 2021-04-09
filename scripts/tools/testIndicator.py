"""
File: testIndicator.py
Brief: A script for looking up data tables supported by the US Census.
Details: Given a Census geocode and a Census indicator code return its value. Intented to be used with searchCensusTables.py.

Author: Charles Herrmann
Date: 9/29/20
"""

import sys
import getopt
import censusdata

# Global Variables
censusType = "acs5"
censusYear = 2019


def printIndicator(geoCode, indicatorCode):
    tmpGeoCode = censusdata.censusgeo([("state", geoCode), ("county", "001")])
    downloaded_data = censusdata.download(
        censusType, censusYear, tmpGeoCode, [indicatorCode], tabletype="subject"
    )
    downloaded_data = downloaded_data.to_dict()
    dl_keys = list(downloaded_data.keys())
    for dl_key in dl_keys:
        print(f"{dl_key}: {downloaded_data[dl_key]}")


def usage():
    print("Usage: searchCensusTables.py -c <Indicator Code>")
    print("Arguments:")
    print("-c: (Required) a census indicator code")


def main(argv):
    geoCode = ""
    indicatorCode = ""

    try:
        opts, args = getopt.getopt(argv, "hg:i:", ["geoCode=", "indicatorCode="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt in "-g":
            geoCode = arg
        elif opt in "-i":
            indicatorCode = arg

    if geoCode == "" or indicatorCode == "":
        usage()
        sys.exit(2)

    printIndicator(geoCode, indicatorCode)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        usage()