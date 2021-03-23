"""
File: genLocations.py
Brief: A script for cacheing geographic locations supported by the US Census.
Details: Looks up all state, county, and place level names and geocodes from the US Census and saves the information to a Json file.

Author: Charles Herrmann
Date: 9/28/20

Variable Descriptions:
 -  locations dictionary = {State_Name: {ID: State_ID, Counties: {County_Name: County_ID}, Places: {Place_Name: Place_ID}}}
    Stores all locations and is saved to a Json file

Reference Code:
 -  The code below is for quickly searching locations available in the census
    geos = censusdata.geographies(censusdata.censusgeo([('zip code tabulation area', '11693')]), 'acs5', 2018)
    g_keys = list(geos.keys())
    g_keys.sort()
    for key in g_keys:
        print(key, '-', geos[key])
"""

import sys
import getopt
import json
import censusdata

# Global Variables
censusType = "acs5"
censusYear = 2018


def printGeos(geo):
    g_keys = list(geo.keys())
    for key in g_keys:
        print(key, geo[key])


def genLocations(dataDir):
    """
    genLocations searches all supported US Census locations and saves them to a Json file.
    """
    print("Acquiring Locations...")

    # temp variable for storing all locations
    locations = []

    # create a list of all state level locations
    states = censusdata.geographies(
        censusdata.censusgeo([("state", "01")]), censusType, censusYear
    )
    s_keys = list(states.keys())
    s_keys.sort()

    # for each state level location...
    count = 0
    for s_key in s_keys:
        # create a temp variable for store state info
        state_level_dict = {}

        # add state name to the dictionary
        state_level_dict["StateName"] = s_key

        # add state ID to the dictionary
        state_level_dict["StateID"] = states[s_key].params()[0][1]

        # add county list to the dictionary
        state_level_dict["Counties"] = []
        counties = censusdata.geographies(
            censusdata.censusgeo(
                [("state", state_level_dict["StateID"]), ("county", "*")]
            ),
            censusType,
            censusYear,
        )
        c_keys = list(counties.keys())
        c_keys.sort()
        for c_key in c_keys:
            county_level_dict = {}
            county_level_dict["CountyName"] = c_key.split(",")[0]
            county_level_dict["CountyID"] = counties[c_key].params()[1][1]
            state_level_dict["Counties"].append(county_level_dict)

        # add place list to the dictionary
        state_level_dict["Places"] = []
        places = censusdata.geographies(
            censusdata.censusgeo(
                [("state", state_level_dict["StateID"]), ("place", "*")]
            ),
            censusType,
            censusYear,
        )
        p_keys = list(places.keys())
        p_keys.sort()
        for p_key in p_keys:
            place_level_dict = {}
            try:
                tmp_place_name = p_key.split(",")[0]
                tmp_index = tmp_place_name.rindex(" ")
                place_level_dict["PlaceName"] = tmp_place_name[0:tmp_index]
            except ValueError:
                place_level_dict["PlaceName"] = p_key.split(",")[0]
            place_level_dict["PlaceID"] = places[p_key].params()[1][1]
            state_level_dict["Places"].append(place_level_dict)

        locations.append(state_level_dict)

        count += 1
        print(f"{count}/{len(s_keys)} Locations Acquiried...")
    print("Finished Acquiring Locations")

    print("Saving Locations...")
    fileName = dataDir + "locations.json"
    with open(fileName, "w") as save_file:
        json.dump(locations, save_file, indent=2)
    print(f"Locations saved to: {fileName}")


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

    genLocations(dataDir)


if __name__ == "__main__":
    main(sys.argv[1:])
