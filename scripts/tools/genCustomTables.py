# [
#   {
#     "SectionName": "Demographics",
#     "SectionTables": [
#       {
#         "TableName": "Race/Ethnicity of Population",
#         "TableIndicators": [
#           {
#             "IndicatorName": "White Percent",
#             "IndicatorFormula": [
#               "B01001A_001E",
#               "B01001_001E",
#               "/",
#               "! 100",
#               "*",
#               "%"
#             ]
#           }
#         ],

import sys
import getopt
import json


def convert(dataDir):
    oldIndicators = None
    newIndicators = []
    with open(dataDir + "customIndicators.json", "r") as loadfile:
        oldIndicators = json.load(loadfile)

    for oldSection in oldIndicators:
        section = {}
        section["SectionName"] = oldSection["SectionName"]
        section["SectionTables"] = []
        for oldTable in oldSection["Indicators"]:
            table = {}
            table["TableName"] = oldTable["IndicatorName"]
            table["TableIndicators"] = []
            keys = list(oldTable.keys())
            for indicatorName in keys[1:]:
                indicator = {}
                indicator["IndicatorName"] = indicatorName
                indicator["IndicatorFormula"] = oldTable[indicatorName]
                table["TableIndicators"].append(indicator)
            section["SectionTables"].append(table)
        newIndicators.append(section)

    fileName = "./customIndicators.json"
    with open(fileName, "w") as save_file:
        json.dump(newIndicators, save_file, indent=2)


def usage():
    print("Usage: genLocations.py -d <dataDir>")
    print("Arguments:\n-d: (Required) path to assets directory")


def main(argv):
    dataDir = ""

    try:
        opts, args = getopt.getopt(argv, "hd:", ["ddir="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt in "-d":
            dataDir = arg

    if dataDir == "":
        usage()
        sys.exit(2)

    convert(dataDir)


if __name__ == "__main__":
    main(sys.argv[1:])