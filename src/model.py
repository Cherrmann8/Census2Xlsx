"""
Author: Charles Herrmann
Date: 9/28/20
Description: A class for quickly gathering census data for a specific geographic level in the US

Variable Descriptions:
 -  census_tables dictionary = {geo: {tableID: downloaded data}}
    The raw data downloaded from the census
 -  data_tables dictionary = {table name: {geo: {label: calculated data}}}
    The calculated data for the output xlsx file

censusdata library reference code:
 -  Example search geography
    censusdata.geographies(
        censusdata.censusgeo([('state', '*'), ('county', '*')]),
        censusType,
        censusYear,
    )
 -  Example download
    censusdata.download(
        censusType,
        censusYear,
        censusdata.censusgeo([('state', '*'), ('county', '*')]),
        tableIDList,
    )
"""

import sys
import getopt
import logging
import json
import censusdata
import xlsxwriter


class CensusModel:
    """CensusModel is the main module for the Census2Xlsx application. Responsible for loading
    cached data, downloading census tables, calculating data tables, and generating the output
    xlsx file. """
    census_type = "acs5"
    census_year = 2018
    census_tables = None
    data_tables = None
    geographies = None
    logger = logging.getLogger("model")
    debug = False

    def __init__(self, debug):
        if debug:
            logging.basicConfig(filename="c2x.log", filemode="w", level=logging.DEBUG)
            print("debug logging turned on...")
        else:
            logging.basicConfig(filename="c2x.log", filemode="w", level=logging.INFO)
            print("debug logging turned off...")

        self.logger.info("Initializing model...")

        # load censusTables.json
        with open("src/data/censusTables.json", "r") as loadfile:
            self.census_tables = json.load(loadfile)
        self.logger.info("Loaded censusTables.json")

        # load dataTableDescriptions.json
        with open("src/data/dataTableDescriptions.json", "r") as loadfile:
            self.data_tables = json.load(loadfile)
        self.logger.info("Loaded dataTableDescriptions.json")

        # load geographies.json
        with open("src/data/geographies.json", "r") as loadfile:
            self.geographies = json.load(loadfile)
        self.logger.info("Loaded geographies.json")

        self.logger.info("Initialized model successfully")

    def gen_data(self, geos, indicators, output_name):
        """
        gen_data will download, calculate, and output data tables to a xlsx file
        :param geos: report area as census geocodes
        :param indicators: selected indicators to be included in the xlsx file
        :param output_name: the name for the output xlsx file
        :return:
        """
        self.logger.info("Generating...")

        # census_tables holds all the raw data collected from the census
        census_tables = {}
        # data_tables holds the edited data calculated from the data dictionary
        data_tables = {}

        # loop through report area locations and obtain all required data from census
        for key in geos.keys():
            self.logger.debug("Requesting data_tables for %s" % key)
            # TODO: check if key is state or zip code
            if geos[key]["selected"]:
                # TODO: load the data in geo and alphabetical order
                # select geography
                geo = censusdata.geographies(
                    censusdata.censusgeo([("state", geos[key]["ID"])]),
                    self.census_type,
                    self.census_year,
                )

                # download census data from selected geography and cached tableIDs
                self.download_data(census_tables, geo, self.census_tables)

        # calculated desired data_tables
        # tmp is used for calculating data_tables. Will be removed at end of calculations
        data_tables["tmp"] = ""
        self.calculate_data(census_tables, data_tables)
        del data_tables["tmp"]

        # save data_tables to xlsx file
        workbook = xlsxwriter.Workbook(output_name)
        self.save_data(workbook, data_tables)
        workbook.close()

        self.logger.info("Generated successfully")

    def download_data(self, data, geo, census_tables):
        self.logger.info("Downloading...")
        # make list of geo's
        geos = list(geo.keys())

        self.logger.debug("Downloading the following TablesIDs: ")
        # for each geo, for each tableType: put all tableID's into one list and download
        detailedTableIDs = []
        concepts = list(census_tables["Detailed Tables"].keys())
        for concept in concepts:
            detailedTableIDs.extend(
                list(census_tables["Detailed Tables"][concept].keys())
            )
            if self.debug:
                self.logger.debug("concept: %s" % concept)
                for tableID in census_tables["Detailed Tables"][concept].keys():
                    self.logger.debug(
                        "    "
                        + tableID
                        + ": "
                        + census_tables["Detailed Tables"][concept][tableID]
                    )

        subjectTableIDs = []
        concepts = list(census_tables["Subject Tables"].keys())
        for concept in concepts:
            subjectTableIDs.extend(list(census_tables["Subject Tables"][concept].keys()))
            if self.debug:
                self.logger.debug("concept: " + concept)
                for tableID in census_tables["Subject Tables"][concept].keys():
                    self.logger.debug(
                        "    "
                        + tableID
                        + ": "
                        + census_tables["Subject Tables"][concept][tableID]
                    )

        dataProfileIDs = []
        concepts = list(census_tables["Data Profiles"].keys())
        for concept in concepts:
            dataProfileIDs.extend(list(census_tables["Data Profiles"][concept].keys()))
            if self.debug:
                self.logger.debug("concept: " + concept)
                for tableID in census_tables["Data Profiles"][concept].keys():
                    self.logger.debug(
                        "    "
                        + tableID
                        + ": "
                        + census_tables["Data Profiles"][concept][tableID]
                    )

        # TODO: This won't work with the planned changed to inputted geo
        # download all censusTables for each geo and add to data
        for g in geos:
            data[g] = {}
            downloaded_data = censusdata.download(
                self.census_type, self.census_year, geo[g], detailedTableIDs
            )
            downloaded_data = downloaded_data.to_dict()
            dl_keys = list(downloaded_data.keys())
            for dl_key in dl_keys:
                data[g][dl_key] = downloaded_data[dl_key][geo[g]]

            downloaded_data = censusdata.download(
                self.census_type,
                self.census_year,
                geo[g],
                subjectTableIDs,
                tabletype="subject",
            )
            downloaded_data = downloaded_data.to_dict()
            dl_keys = list(downloaded_data.keys())
            for dl_key in dl_keys:
                data[g][dl_key] = downloaded_data[dl_key][geo[g]]

            downloaded_data = censusdata.download(
                self.census_type,
                self.census_year,
                geo[g],
                dataProfileIDs,
                tabletype="profile",
            )
            downloaded_data = downloaded_data.to_dict()
            dl_keys = list(downloaded_data.keys())
            for dl_key in dl_keys:
                data[g][dl_key] = downloaded_data[dl_key][geo[g]]

        self.logger.info("Downloaded successfully")

    def calculate_formula(self, formula, geo, census_table, data_tables):
        """
        calculate_formula calculates a specific indicator for data_tables
        :param formula: a string showing how to calculate this specific indicator
        :param geo: the location
        :param census_table: the census data to use in the calculation
        :param data_tables: the calculated indicators
        """
        calculator = []
        for item in formula:
            if len(item) == 1:
                if item == "s":
                    if data_tables["tmp"] != "":
                        self.logger.warning("Tried to overwrite the tmp variable")
                        sys.exit(2)
                    data_tables["tmp"] = calculator[len(calculator) - 1]
                    # print('=s=', dataTables['tmp'])
                if item == "l":
                    # print('=l=', dataTables['tmp'])
                    if data_tables["tmp"] == "":
                        self.logger.warning("Tried to load tmp variable but non exists")
                        sys.exit(2)
                    calculator.append(data_tables["tmp"])
                    data_tables["tmp"] = ""
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
                        self.logger.warning("Divide non-zero by zero")
                        self.logger.warning("%s / %s" % (str(a), str(b)))
                        if a == 0:
                            calculator.append(0)
                    else:
                        calculator.append(a / b)
            else:
                if item[0] == "!":
                    calculator.append(int(item.split(" ")[1]))
                else:
                    calculator.append(census_table[geo][item])
            self.logger.debug(calculator)
            if data_tables["tmp"] != "":
                self.logger.debug("tmp: %s" % str(data_tables["tmp"]))
        return calculator.pop()

    def calculate_data(self, census_tables, data_tables):
        """
        calculate_data transforms the census data into indicators
        :param census_tables: the downloaded raw data from the census
        :param data_tables: the calculated indicators for the xlsx
        """
        self.logger.info("Calculating...")
        ct_keys = list(census_tables.keys())
        dt_keys = list(self.data_tables.keys())
        for dt_key in dt_keys:
            if len(self.data_tables[dt_key]) > 0:
                data_tables[dt_key] = {}
                dt_labels = list(self.data_tables[dt_key].keys())
                for data_key in ct_keys:
                    data_tables[dt_key][data_key] = {}
                    for dt_label in dt_labels:
                        self.logger.debug(
                            "Model calculating "
                            + dt_key
                            + "-"
                            + data_key
                            + "-"
                            + dt_label
                        )
                        data_tables[dt_key][data_key][
                            dt_label
                        ] = self.calculate_formula(
                            self.data_tables[dt_key][dt_label],
                            data_key,
                            census_tables,
                            data_tables,
                        )

        self.logger.info("Calculated successfully")

    def save_data(self, workbook, data_tables):
        """
        save_data creates a new xlsx file filled with data tables
        :param workbook: the xlsx file to save the data_tables to
        :param data_tables: the calculated indicators of interest
        """
        self.logger.info("Saving...")
        worksheet = workbook.add_worksheet()
        header_format = workbook.add_format(
            {
                "font_name": "Times New Roman",
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
                "border": True,
                "pattern": 1,
                "bg_color": "#d3d3d3",
            }
        )
        label_format = workbook.add_format(
            {
                "font_name": "Times New Roman",
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
                "border": True,
                "pattern": 1,
                "bg_color": "#f8f8f8",
            }
        )
        geo_format = workbook.add_format(
            {
                "font_name": "Times New Roman",
                "bold": False,
                "align": "left",
                "valign": "bottom",
                "text_wrap": False,
                "border": True,
            }
        )
        body_format = workbook.add_format(
            {
                "font_name": "Times New Roman",
                "bold": False,
                "align": "right",
                "valign": "bottom",
                "text_wrap": False,
                "border": True,
            }
        )

        row = 0
        col = 0
        titles = list(data_tables.keys())
        for title in titles:
            geos = list(data_tables[title].keys())
            labels = list(data_tables[title][geos[0]].keys())
            worksheet.merge_range(row, 0, row, len(labels), title, header_format)
            row += 1
            worksheet.write(row, col, "Report Area", label_format)
            for label in labels:
                worksheet.write(row, col + 1, label, label_format)
                col += 1
            row += 1
            col = 0
            for geo in geos:
                worksheet.write(row, col, geo, geo_format)
                col += 1
                for label in labels:
                    worksheet.write(row, col, data_tables[title][geo][label], body_format)
                    col += 1
                row += 1
                col = 0
            row += 1
        self.logger.info("Saved successfully")


def main(debug):
    """
    This main function was developed to test the CensusModel class. This function contains almost
    the exact code found in CensusModel.genData(). The only modification is hard-coded geos and
    data_tables for debugging purposes. The debug parameter sets the CensusModel to debug mode.
    """
    census_model = CensusModel(debug)
    data = {}

    # Acquire geography
    tmp_geo = censusdata.geographies(
        censusdata.censusgeo([("zip code tabulation area", "11693")]),
        census_model.census_type,
        census_model.census_year,
    )
    # download census data from selected geography and cached tableIDs
    census_model.download_data(data, tmp_geo, census_model.census_tables)

    # vvv ALL TEMP GEOS IN THIS SECTION vvv
    tmp_geo = censusdata.geographies(
        censusdata.censusgeo([("state", "36"), ("county", "081")]),
        census_model.census_type,
        census_model.census_year,
    )
    census_model.download_data(data, tmp_geo, census_model.census_tables)
    tmp_geo = censusdata.geographies(
        censusdata.censusgeo([("state", "36")]), census_model.census_type, census_model.census_year
    )
    census_model.download_data(data, tmp_geo, census_model.census_tables)
    # ^^^ ALL TEMP GEOS IN THIS SECTION ^^^

    # calculated desired data_tables
    data_tables = {
        "tmp": ""
    }  # tmp is used for calculating data_tables. Will be removed at end of calculations
    census_model.calculate_data(data, data_tables)
    del data_tables["tmp"]

    # save data_tables to xlsx file
    workbook = xlsxwriter.Workbook("output.xlsx")
    census_model.save_data(workbook, data_tables)
    workbook.close()


if __name__ == "__main__":
    # Comment out the following line if this isn't the entry file or if you don't want logging
    # logging.basicConfig(filename='c2x.log', filemode='w', level=logging.INFO)

    DAT_DIR = ""
    LOG_DIR = ""
    OUT_DIR = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:l:o:", ["ddir=", "ldir=", "odir="])
    except getopt.GetoptError:
        print("model.py -l <logDir> -o <outputDir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("model.py -l <logDir> -o <outputDir>")
            sys.exit()
        elif opt in "-d":
            DAT_DIR = arg
        elif opt in "-l":
            LOG_DIR = arg
        elif opt in "-o":
            OUT_DIR = arg

    # main(sys.argv[1:])
