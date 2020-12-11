import sys
import getopt
import censusdata
import json

"""
Author: Charles Herrmann
Date: 9/28/20
Description: A script for cacheing data to Json files to speed up the application.
    The first Json file is censusTables.json which stores Table IDs from the census website.
    The second Json file is geographies.json which stores all the available locations. 

Variable Descriptions:
 -  Tables dictionary = {Concept: {TableID: Label}}
    The Table IDs on the census website
 -  Geos dictionary = {State_Name: {ID: State_ID, Counties: {County_Name: County_ID}}}
    The Geographies available for the user

Reference Code:
 -  Example print json to console
    print(json.dumps(tables, indent=4))
 -  Code used to load the censusTables.json file
    with open('censusTables.json', 'r') as loadfile:
       loadedTables = json.load(loadfile)
 -  Example search
    printTableSearch('searchTerm')
 -  Example print table
    concept, var_keys, var_values = getTable('tableID')
    printTableLabels(concept, var_keys, var_values)
 -  The code below is for quickly searching geographies available in the census
    # geos = censusdata.geographies(censusdata.censusgeo([('zip code tabulation area', '11693')]), 'acs5', 2018)
    # g_keys = list(geos.keys())
    # g_keys.sort()
    # for key in g_keys:
    #     print(key, '-', geos[key])

"""

# Global Variables
censusType = "acs5"
censusYear = 2018


def printTableLabels(concept, var_keys, var_values):
    print(concept)
    for i in range(len(var_values)):
        print(i, ": ", var_values[i], " - ", var_keys[i])


def printTableSearch(label, tableType):
    tmp = censusdata.search(censusType, censusYear, "label", label, tabletype=tableType)
    for item in tmp:
        print(item)


def printTableCheck(tables):
    concepts = 0  # total number of concepts
    labels = 0  # total number of labels
    for tableType in tables.keys():
        table_keys = list(tables[tableType].keys())
        for i in range(len(table_keys)):
            concepts += 1
            labels += len(tables[tableType][table_keys[i]])
    print("Number of concepts:", concepts, "\nNumber of labels:", labels)


def printTable(tables):
    for tableType in tables.keys():
        for concept in tables[tableType].keys():
            print(concept)
            for label in tables[tableType][concept].keys():
                print(label + ": " + tables[tableType][concept][label])


def printGeos(geo):
    g_keys = list(geo.keys())
    for key in g_keys:
        print(key, geo[key])


def getLabel(var_values, index):
    label = str(var_values[index]["label"]).split("!")
    while "" in label:
        label.remove("")
    return " ".join(label)


def getTable(tableID):
    var = censusdata.censustable(censusType, censusYear, tableID)
    var_keys = list(var.keys())
    var_values = list(var.values())
    concept = var_values[0]["concept"]
    return concept, var_keys, var_values


def fillRaceAgeTables(tables, concept, var_keys, var_values):
    # make new concept in tables dictionary
    tables["Detailed Tables"][concept] = {}

    # total
    tables["Detailed Tables"][concept][var_keys[0]] = getLabel(var_values, 0)

    # male 0-4
    tables["Detailed Tables"][concept][var_keys[2]] = getLabel(var_values, 2)
    # male 5-9
    tables["Detailed Tables"][concept][var_keys[3]] = getLabel(var_values, 3)
    # male 10-14
    tables["Detailed Tables"][concept][var_keys[4]] = getLabel(var_values, 4)
    # male 15-17
    tables["Detailed Tables"][concept][var_keys[5]] = getLabel(var_values, 5)

    # female 0-4
    tables["Detailed Tables"][concept][var_keys[17]] = getLabel(var_values, 17)
    # female 5-9
    tables["Detailed Tables"][concept][var_keys[18]] = getLabel(var_values, 18)
    # female 10-14
    tables["Detailed Tables"][concept][var_keys[19]] = getLabel(var_values, 19)
    # female 15-17
    tables["Detailed Tables"][concept][var_keys[20]] = getLabel(var_values, 20)


def fillPovertyRaceTables(tables, concept, var_keys, var_values):
    # make new concept in tables dictionary
    tables["Detailed Tables"][concept] = {}

    # total
    tables["Detailed Tables"][concept][var_keys[0]] = getLabel(var_values, 0)
    # total in poverty
    tables["Detailed Tables"][concept][var_keys[1]] = getLabel(var_values, 1)
    # under age 6 in poverty
    tables["Detailed Tables"][concept][var_keys[2]] = getLabel(var_values, 2)
    # 6-11 in poverty
    tables["Detailed Tables"][concept][var_keys[3]] = getLabel(var_values, 3)
    # 12-17 in poverty
    tables["Detailed Tables"][concept][var_keys[4]] = getLabel(var_values, 4)


def fillPovertyFamilyTables(tables, concept, var_keys, var_values):
    # make new concept in tables dictionary
    tables["Detailed Tables"][concept] = {}

    # total families in poverty
    tables["Detailed Tables"][concept][var_keys[1]] = getLabel(var_values, 1)
    # married-couple in poverty
    tables["Detailed Tables"][concept][var_keys[2]] = getLabel(var_values, 2)
    # single father in poverty
    tables["Detailed Tables"][concept][var_keys[9]] = getLabel(var_values, 9)
    # single mother in poverty
    tables["Detailed Tables"][concept][var_keys[15]] = getLabel(var_values, 15)


def fillTables(tables):
    # SEX BY AGE - B01001
    concept, var_keys, var_values = getTable("B01001")
    tables["Detailed Tables"][concept] = {}  # make new concept in tables dictionary
    tables["Detailed Tables"][concept][var_keys[0]] = getLabel(var_values, 0)  # total
    tables["Detailed Tables"][concept][var_keys[2]] = getLabel(
        var_values, 2
    )  # male 0-4
    tables["Detailed Tables"][concept][var_keys[3]] = getLabel(
        var_values, 3
    )  # male 5-9
    tables["Detailed Tables"][concept][var_keys[4]] = getLabel(
        var_values, 4
    )  # male 10-14
    tables["Detailed Tables"][concept][var_keys[5]] = getLabel(
        var_values, 5
    )  # male 15-17
    tables["Detailed Tables"][concept][var_keys[26]] = getLabel(
        var_values, 26
    )  # female 0-4
    tables["Detailed Tables"][concept][var_keys[27]] = getLabel(
        var_values, 27
    )  # female 5-9
    tables["Detailed Tables"][concept][var_keys[28]] = getLabel(
        var_values, 28
    )  # female 10-14
    tables["Detailed Tables"][concept][var_keys[29]] = getLabel(
        var_values, 29
    )  # female 15-17

    # SEX BY AGE (WHITE ALONE) - B01001A
    concept, var_keys, var_values = getTable("B01001A")
    fillRaceAgeTables(tables, concept, var_keys, var_values)

    # SEX BY AGE (BLACK OR AFRICAN AMERICAN ALONE) - B01001B
    concept, var_keys, var_values = getTable("B01001B")
    fillRaceAgeTables(tables, concept, var_keys, var_values)

    # SEX BY AGE (AMERICAN INDIAN AND ALASKA NATIVE ALONE) - B01001C
    concept, var_keys, var_values = getTable("B01001C")
    fillRaceAgeTables(tables, concept, var_keys, var_values)

    # SEX BY AGE (ASIAN ALONE) - B01001D
    concept, var_keys, var_values = getTable("B01001D")
    fillRaceAgeTables(tables, concept, var_keys, var_values)

    # SEX BY AGE (NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER ALONE) - B01001E
    concept, var_keys, var_values = getTable("B01001E")
    fillRaceAgeTables(tables, concept, var_keys, var_values)

    # SEX BY AGE (TWO OR MORE RACES) - B01001G
    concept, var_keys, var_values = getTable("B01001G")
    fillRaceAgeTables(tables, concept, var_keys, var_values)

    # SEX BY AGE (WHITE ALONE, NOT HISPANIC OR LATINO) - B01001H
    concept, var_keys, var_values = getTable("B01001H")
    fillRaceAgeTables(tables, concept, var_keys, var_values)

    # SEX BY AGE (HISPANIC OR LATINO) - B01001I
    concept, var_keys, var_values = getTable("B01001I")
    fillRaceAgeTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE - B17020
    concept, var_keys, var_values = getTable("B17020")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE (WHITE ALONE) - B17020A
    concept, var_keys, var_values = getTable("B17020A")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE (BLACK OR AFRICAN AMERICAN ALONE) - B17020B
    concept, var_keys, var_values = getTable("B17020B")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE (AMERICAN INDIAN AND ALASKA NATIVE ALONE) - B17020C
    concept, var_keys, var_values = getTable("B17020C")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE (ASIAN ALONE) - B17020D
    concept, var_keys, var_values = getTable("B17020D")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE (NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER ALONE) - B17020E
    concept, var_keys, var_values = getTable("B17020E")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE (TWO OR MORE RACES) - B17020G
    concept, var_keys, var_values = getTable("B17020G")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE (WHITE ALONE, NOT HISPANIC OR LATINO) - B17020H
    concept, var_keys, var_values = getTable("B17020H")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS BY AGE (HISPANIC OR LATINO) - B17020I
    concept, var_keys, var_values = getTable("B17020I")
    fillPovertyRaceTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY FAMILY TYPE BY PRESENCE OF RELATED CHILDREN UNDER 18 YEARS BY AGE OF RELATED CHILDREN - B17010
    concept, var_keys, var_values = getTable("B17010")
    fillPovertyFamilyTables(tables, concept, var_keys, var_values)

    # POVERTY STATUS IN THE PAST 12 MONTHS - S1701_C01
    concept, var_keys, var_values = getTable("S1701_C01")
    tables["Subject Tables"][concept] = {}
    tables["Subject Tables"][concept][var_keys[37]] = getLabel(var_values, 37)
    tables["Subject Tables"][concept][var_keys[38]] = getLabel(var_values, 38)
    tables["Subject Tables"][concept][var_keys[39]] = getLabel(var_values, 39)

    # WOMEN 15 TO 50 YEARS WHO HAD A BIRTH IN THE PAST 12 MONTHS BY MARITAL STATUS AND AGE - B13002
    concept, var_keys, var_values = getTable("B13002")
    tables["Detailed Tables"][concept] = {}
    tables["Detailed Tables"][concept][var_keys[6]] = getLabel(var_values, 6)

    # WOMEN 15 TO 50 YEARS WHO HAD A BIRTH IN THE PAST 12 MONTHS BY MARITAL STATUS AND POVERTY STATUS IN THE PAST 12 MONTHS - B13010
    concept, var_keys, var_values = getTable("B13010")
    tables["Detailed Tables"][concept] = {}
    tables["Detailed Tables"][concept][var_keys[3]] = getLabel(var_values, 3)
    tables["Detailed Tables"][concept][var_keys[7]] = getLabel(var_values, 7)

    # WOMEN 15 TO 50 YEARS WHO HAD A BIRTH IN THE PAST 12 MONTHS BY MARITAL STATUS AND EDUCATIONAL ATTAINMENT - B13014
    concept, var_keys, var_values = getTable("B13014")
    tables["Detailed Tables"][concept] = {}
    tables["Detailed Tables"][concept][var_keys[3]] = getLabel(var_values, 3)
    tables["Detailed Tables"][concept][var_keys[9]] = getLabel(var_values, 9)

    # HS eligible - B13016
    concept, var_keys, var_values = getTable("B13016")
    tables["Detailed Tables"][concept] = {}
    tables["Detailed Tables"][concept][var_keys[1]] = getLabel(var_values, 1)

    # PUBLIC HEALTH INSURANCE STATUS BY SEX BY AGE - B27003
    concept, var_keys, var_values = getTable("B27003")
    tables["Detailed Tables"][concept] = {}
    tables["Detailed Tables"][concept][var_keys[3]] = getLabel(var_values, 3)
    tables["Detailed Tables"][concept][var_keys[6]] = getLabel(var_values, 6)
    tables["Detailed Tables"][concept][var_keys[9]] = getLabel(var_values, 9)
    tables["Detailed Tables"][concept][var_keys[12]] = getLabel(var_values, 12)
    tables["Detailed Tables"][concept][var_keys[15]] = getLabel(var_values, 15)
    tables["Detailed Tables"][concept][var_keys[18]] = getLabel(var_values, 18)
    tables["Detailed Tables"][concept][var_keys[21]] = getLabel(var_values, 21)
    tables["Detailed Tables"][concept][var_keys[24]] = getLabel(var_values, 24)
    tables["Detailed Tables"][concept][var_keys[27]] = getLabel(var_values, 27)
    tables["Detailed Tables"][concept][var_keys[31]] = getLabel(var_values, 31)
    tables["Detailed Tables"][concept][var_keys[34]] = getLabel(var_values, 34)
    tables["Detailed Tables"][concept][var_keys[37]] = getLabel(var_values, 37)
    tables["Detailed Tables"][concept][var_keys[40]] = getLabel(var_values, 40)
    tables["Detailed Tables"][concept][var_keys[43]] = getLabel(var_values, 43)
    tables["Detailed Tables"][concept][var_keys[46]] = getLabel(var_values, 46)
    tables["Detailed Tables"][concept][var_keys[49]] = getLabel(var_values, 49)
    tables["Detailed Tables"][concept][var_keys[52]] = getLabel(var_values, 52)
    tables["Detailed Tables"][concept][var_keys[55]] = getLabel(var_values, 55)

    # OWN CHILDREN UNDER 18 YEARS BY FAMILY TYPE AND AGE - B09002
    concept, var_keys, var_values = getTable("B09002")
    tables["Detailed Tables"][concept] = {}
    tables["Detailed Tables"][concept][var_keys[1]] = getLabel(var_values, 1)
    tables["Detailed Tables"][concept][var_keys[2]] = getLabel(var_values, 2)
    tables["Detailed Tables"][concept][var_keys[3]] = getLabel(var_values, 3)
    tables["Detailed Tables"][concept][var_keys[4]] = getLabel(var_values, 4)
    tables["Detailed Tables"][concept][var_keys[8]] = getLabel(var_values, 8)
    tables["Detailed Tables"][concept][var_keys[9]] = getLabel(var_values, 9)
    tables["Detailed Tables"][concept][var_keys[10]] = getLabel(var_values, 10)
    tables["Detailed Tables"][concept][var_keys[11]] = getLabel(var_values, 11)
    tables["Detailed Tables"][concept][var_keys[14]] = getLabel(var_values, 14)
    tables["Detailed Tables"][concept][var_keys[15]] = getLabel(var_values, 15)
    tables["Detailed Tables"][concept][var_keys[16]] = getLabel(var_values, 16)
    tables["Detailed Tables"][concept][var_keys[17]] = getLabel(var_values, 17)

    # POPULATION UNDER 18 YEARS BY AGE - B09001
    concept, var_keys, var_values = getTable("B09001")
    tables["Detailed Tables"][concept] = {}
    tables["Detailed Tables"][concept][var_keys[0]] = getLabel(var_values, 0)
    tables["Detailed Tables"][concept][var_keys[2]] = getLabel(var_values, 2)
    tables["Detailed Tables"][concept][var_keys[3]] = getLabel(var_values, 3)
    tables["Detailed Tables"][concept][var_keys[4]] = getLabel(var_values, 4)

    # PRESENCE OF OWN CHILDREN UNDER 18 YEARS BY FAMILY TYPE BY EMPLOYMENT STATUS - B23007
    concept, var_keys, var_values = getTable("B23007")
    tables["Detailed Tables"][concept] = {}
    tables["Detailed Tables"][concept][var_keys[6]] = getLabel(var_values, 6)
    tables["Detailed Tables"][concept][var_keys[22]] = getLabel(var_values, 22)
    tables["Detailed Tables"][concept][var_keys[27]] = getLabel(var_values, 27)

    # SELECTED ECONOMIC CHARACTERISTICS - DP03
    concept, var_keys, var_values = getTable("DP03")
    tables["Data Profiles"][concept] = {}
    tables["Data Profiles"][concept][var_keys[4]] = getLabel(var_values, 4)
    tables["Data Profiles"][concept][var_keys[6]] = getLabel(var_values, 6)
    tables["Data Profiles"][concept][var_keys[8]] = getLabel(var_values, 8)
    tables["Data Profiles"][concept][var_keys[9]] = getLabel(var_values, 9)

    # EDUCATIONAL ATTAINMENT - S1501
    concept, var_keys, var_values = getTable("S1501_C01")
    tables["Subject Tables"][concept] = {}
    tables["Subject Tables"][concept][var_keys[5]] = getLabel(var_values, 5)
    tables["Subject Tables"][concept][var_keys[6]] = getLabel(var_values, 6)
    tables["Subject Tables"][concept][var_keys[7]] = getLabel(var_values, 7)
    tables["Subject Tables"][concept][var_keys[8]] = getLabel(var_values, 8)
    tables["Subject Tables"][concept][var_keys[9]] = getLabel(var_values, 9)
    tables["Subject Tables"][concept][var_keys[10]] = getLabel(var_values, 10)
    tables["Subject Tables"][concept][var_keys[11]] = getLabel(var_values, 11)
    tables["Subject Tables"][concept][var_keys[12]] = getLabel(var_values, 12)

    # SELECTED CHARACTERISTICS OF HEALTH INSURANCE COVERAGE IN THE UNITED STATES - S2701
    concept, var_keys, var_values = getTable("S2701_C05")
    tables["Subject Tables"][concept] = {}
    tables["Subject Tables"][concept][var_keys[0]] = getLabel(var_values, 0)
    tables["Subject Tables"][concept][var_keys[1]] = getLabel(var_values, 1)
    tables["Subject Tables"][concept][var_keys[10]] = getLabel(var_values, 10)

    # LIMITED ENGLISH SPEAKING HOUSEHOLDS - S1602
    concept, var_keys, var_values = getTable("S1602_C04")
    tables["Subject Tables"][concept] = {}
    tables["Subject Tables"][concept][var_keys[0]] = getLabel(var_values, 0)


def genCensusTables(dataDir):
    tables = {"Detailed Tables": {}, "Subject Tables": {}, "Data Profiles": {}}

    print("Acquiring Data Tables...")
    fillTables(tables)
    print("Done")

    printTableCheck(tables)
    printTable(tables)

    with open(dataDir + "censusTables.json", "w") as save_file:
        json.dump(tables, save_file, indent=4)


def genGeographies(dataDir):
    geos = {}

    print("Acquiring Geographies...")
    states = censusdata.geographies(
        censusdata.censusgeo([("state", "*")]), censusType, censusYear
    )
    s_keys = list(states.keys())
    s_keys.sort()
    count = 0
    for s_key in s_keys:
        geos[s_key] = {"ID": states[s_key].params()[0][1]}
        geos[s_key]["Counties"] = {}
        counties = censusdata.geographies(
            censusdata.censusgeo([("state", geos[s_key]["ID"]), ("county", "*")]),
            censusType,
            censusYear,
        )
        c_keys = list(counties.keys())
        c_keys.sort()
        for c_key in c_keys:
            geos[s_key]["Counties"][c_key.split(",")[0]] = counties[c_key].params()[1][
                1
            ]
        geos[s_key]["Places"] = {}
        places = censusdata.geographies(
            censusdata.censusgeo([("state", geos[s_key]["ID"]), ("place", "*")]),
            censusType,
            censusYear,
        )
        p_keys = list(places.keys())
        p_keys.sort()
        for p_key in p_keys:
            geos[s_key]["Places"][p_key.split(",")[0]] = places[p_key].params()[1][1]
        count += 1
        print(count, len(s_keys))
    print("Done")

    with open("geographies.json", "w") as save_file:
        json.dump(geos, save_file, indent=4)

    # TODO remove this eventually (used for searching census database geographies)
    # tmp_loc = censusdata.geographies(censusdata.censusgeo([('state', '35'), ('place', '*')]), censusType, censusYear)
    # print(censusdata.censusgeo([('state', '35'), ('place', '*')]).sumlevel())
    # l_keys = list(tmp_loc.keys())
    # l_keys.sort()
    # for l_key in l_keys:
    #     print(l_key, tmp_loc[l_key])


def main(argv):
    dataDir = ""
    try:
        opts, args = getopt.getopt(argv, "hd:", ["ddir="])
    except getopt.GetoptError:
        print("tools.py -d <dataDir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("tools.py -d <dataDir>")
            sys.exit()
        elif opt in "-d":
            dataDir = arg + "/"

    genCensusTables(dataDir)
    genGeographies(dataDir)

    # TODO: Make this its own function
    # """ The lines below are for searching for new table IDs """
    # printTableSearch('INSURANCE', 'subject')
    # concept, var_keys, var_values = getTable('S1602_C04')
    # printTableLabels(concept, var_keys, var_values)


if __name__ == "__main__":
    main(sys.argv[1:])
