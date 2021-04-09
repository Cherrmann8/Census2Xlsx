"""
File: searchCensusTables.py
Brief: A script for looking up data tables supported by the US Census.
Details: Given a label and census table type, return all match census tables.

Author: Charles Herrmann
Date: 9/29/20
"""

import sys
import getopt
import censusdata

# Global Variables
censusType = "acs5"
censusYear = 2019


def printTableSearch(label, tableType):
    tmp = censusdata.search(censusType, censusYear, "label", label, tabletype=tableType)
    for item in tmp:
        print(item)


def usage():
    print("Usage: searchCensusTables.py -s <Search Phrase> -t <Table Type>")
    print("Arguments:")
    print("-s: (Required) a phrase thats used to describe a Census data table")
    print(
        "-t: (Required) The type of ACS table. Options are ‘detail’ (detail tables), ‘subject’ (subject tables), ‘profile’ (data profile tables), ‘cprofile’ (comparison profile tables)"
    )


def main(argv):
    searchPhrase = ""
    tableType = ""

    try:
        opts, args = getopt.getopt(argv, "hs:t:", ["searchPhrase=", "tableType="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt in "-s":
            searchPhrase = arg
        elif opt in "-t":
            tableType = arg

    if searchPhrase == "" or tableType == "":
        usage()
        sys.exit(2)

    printTableSearch(searchPhrase, tableType)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        usage()