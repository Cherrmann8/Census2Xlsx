import censusdata
import json
import xlsxwriter
from tools import printTableCheck
import logging

"""
Author: Charles Herrmann
Date: 9/28/20
Description: A script for quickly gathering community needs assessment data for a specific geographic level in the US

Variable Descriptions:
 -  Data dictionary = {geo: {tableID: downloaded data}}
    The raw data downloaded from the census
 -  DataTables dictionary = {table name: {geo: {label: calculated data}}}
    The calculated data for the Databook

Census library Reference Code:
 -  Example search geography
    censusdata.geographies(censusdata.censusgeo([('state', '*'), ('county', '*')]), censusType, censusYear)
 -  Example download
    censusdata.download(censusType, censusYear, censusdata.censusgeo([('state', '*'), ('county', '*')]), tableIDList)
"""

# Global Variables
censusType = 'acs5'
censusYear = 2018
xlsxFileName = 'Generated_Databook.xlsx'
verbose = False
logger = logging.getLogger('model')


def downloadData(data, geo, censusTables):
    # make list of geo's
    geos = list(geo.keys())

    # put all tableID's into one list
    concepts = list(censusTables.keys())
    all_TableIDs = []
    for concept in concepts:
        all_TableIDs.extend(list(censusTables[concept].keys()))

    # download all censusTables for each geo and add to data
    for g in geos:
        data[g] = {}
        dl = censusdata.download(censusType, censusYear, geo[g], all_TableIDs)
        dl = dl.to_dict()
        dl_keys = list(dl.keys())
        for dl_key in dl_keys:
            data[g][dl_key] = dl[dl_key][geo[g]]


def calculateFormula(formula, geo, data, dataTables):
    calculator = []
    for item in formula:
        if len(item) == 1:
            if item == "s":
                if dataTables["tmp"] != "":
                    logger.warning("Tried to overwrite the tmp variable")
                    exit(1)
                dataTables["tmp"] = calculator[len(calculator) - 1]
                # print("=s=", dataTables["tmp"])
            if item == "l":
                # print("=l=", dataTables["tmp"])
                if dataTables["tmp"] == "":
                    logger.warning("Tried to load tmp variable but non exists")
                    exit(1)
                calculator.append(dataTables["tmp"])
                dataTables["tmp"] = ""
            if item == "+":
                b = calculator.pop()
                a = calculator.pop()
                calculator.append(a + b)
            if item == "-":
                b = calculator.pop()
                a = calculator.pop()
                calculator.append(a - b)
            if item == "/":
                b = calculator.pop()
                a = calculator.pop()
                if b == 0:
                    logger.warning("Divide non-zero by zero")
                    logger.warning(a + " / " + b)
                    if a == 0:
                        calculator.append(0)
                else:
                    calculator.append(a / b)
        else:
            if item[0] == '!':
                calculator.append(int(item.split(" ")[1]))
            else:
                calculator.append(data[geo][item])
        if verbose:
            print(calculator)
            if dataTables["tmp"] != "":
                print("tmp:", dataTables["tmp"])
    return calculator.pop()


def calculateData(data, dtDesc, dataTables):
    data_keys = list(data.keys())
    dtDesc_keys = list(dtDesc.keys())
    for dtDesc_key in dtDesc_keys:
        if len(dtDesc[dtDesc_key]) > 0:
            dataTables[dtDesc_key] = {}
            dtDesc_labels = list(dtDesc[dtDesc_key].keys())
            for data_key in data_keys:
                dataTables[dtDesc_key][data_key] = {}
                for dtDesc_label in dtDesc_labels:
                    if verbose:
                        print("calculating", dtDesc_key, "-", data_key, "-", dtDesc_label)
                    dataTables[dtDesc_key][data_key][dtDesc_label] = calculateFormula(dtDesc[dtDesc_key][dtDesc_label], data_key, data, dataTables)


def saveData(workbook, dataTables):
    worksheet = workbook.add_worksheet()
    HeaderFormat = workbook.add_format({'font_name': 'Times New Roman', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True, 'pattern': 1, 'bg_color': '#d3d3d3'})
    LabelFormat = workbook.add_format({'font_name': 'Times New Roman', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True, 'pattern': 1, 'bg_color': '#f8f8f8'})
    GeoFormat = workbook.add_format({'font_name': 'Times New Roman', 'bold': False, 'align': 'left', 'valign': 'bottom', 'text_wrap': False, 'border': True})
    BodyFormat = workbook.add_format({'font_name': 'Times New Roman', 'bold': False, 'align': 'right', 'valign': 'bottom', 'text_wrap': False, 'border': True})

    row = 0
    col = 0
    titles = list(dataTables.keys())
    for title in titles:
        geos = list(dataTables[title].keys())
        labels = list(dataTables[title][geos[0]].keys())
        worksheet.merge_range(row, 0, row, len(labels), title, HeaderFormat)
        row += 1
        worksheet.write(row, col, "Report Area", LabelFormat)
        for label in labels:
            worksheet.write(row, col+1, label, LabelFormat)
            col += 1
        row += 1
        col = 0
        for geo in geos:
            worksheet.write(row, col, geo, GeoFormat)
            col += 1
            for label in labels:
                worksheet.write(row, col, dataTables[title][geo][label], BodyFormat)
                col += 1
            row += 1
            col = 0
        row += 1


def main():
    # load censusTables.json
    logger.info("Loading Json files...")

    with open('censusTables.json', 'r') as loadfile:
        censusTables = json.load(loadfile)
    # for error checking
    # print censusTables and dimensions
    if verbose:
        print(json.dumps(censusTables, indent=4))
        printTableCheck(censusTables)

    # load dataTableDescriptions.json
    with open("dataTableDescriptions.json", 'r') as loadfile:
        dataTableDesc = json.load(loadfile)
    if verbose:
        print(json.dumps(dataTableDesc, indent=4))

    # select geography
    # TODO finish UI
    # tmp_geo is for testing.
    tmp_geo = censusdata.geographies(censusdata.censusgeo([('state', '28'), ('county', '023')]), censusType, censusYear)

    # download census data from selected geography and cached tableIDs
    logger.info("Downloading data from Census...")
    data = {}
    downloadData(data, tmp_geo, censusTables)

    if verbose:
        print(json.dumps(data, indent=4))

    # calculated desired dataTables
    logger.info("Calculating dataTables...")
    dataTables = {"tmp": ""}  # tmp is used for calculating dataTables. Will be removed at end of calculations
    calculateData(data, dataTableDesc, dataTables)
    del dataTables["tmp"]

    # save dataTables to xlsx file
    logger.info("Saving dataTables...")
    workbook = xlsxwriter.Workbook(xlsxFileName)
    saveData(workbook, dataTables)
    workbook.close()

    logger.info("Model done")


if __name__ == '__main__':
    main()
    # geos = censusdata.geographies(censusdata.censusgeo([('state', '28'), ('county', '*')]), censusType, censusYear)
    # g_keys = list(geos.keys())
    # g_keys.sort()
    # for key in g_keys:
    #     print(key, "-", geos[key])
