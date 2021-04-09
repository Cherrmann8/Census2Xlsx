"""
File: census2xlsx.py
Brief: A script for collecting US census data
Details: Given a set of locations and indicators, will download census data for each location,
    calculate the specified indicators, and save the indicators to a .xlsx file.

Author: Charles Herrmann
Date: 9/28/20

Terminology:
 -  Report Area: A set of locations.
 -  Location: A geographic location described by a census geocode. Locations can represent a variety
        of geographic levels defined but the US census (state, county, or place).
 -  Table: A set of related indicators.
 -  Indicator: A data point indicating the state or level of something.

Important Variable Descriptions:
 -  report_area = [(location_name, geographic_level, primary_ID, secondary_ID)]
 -  selected_indicators[()]
 -  census_tables = {geo_name: {indicator_ID: downloaded_data}}
        The raw data downloaded from the censusdata package
 -  custom_tables = {section_name: {table_name: {location_name: {indicator_name: calculated_data}}}}
        The calculated data for the output xlsx file

Censusdata Package Reference Code:
 -  Example geography search 
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


class Census2Xlsx:
    # files containing cached info on geocodes, census table IDs, and custom table formulas
    census_tables_file = None
    custom_tables_file = None

    # censusdata package variables
    # TODO: dynamically set census_type and census_year
    census_type = "acs5"
    census_year = 2019
    detailed_table_IDs = []
    subject_table_IDs = []
    data_profile_IDs = []

    # flags and logger object
    logFlag = True
    debugFlag = True
    verboseFlag = False
    logger = None

    def __init__(self, data_dir, log_dir=""):
        # setup logging if logFlag is active
        if self.logFlag:
            tmpLevel = logging.INFO
            # set logging level to DEBUG if debugFlag is active
            if self.debugFlag:
                tmpLevel = logging.DEBUG

            logging.basicConfig(
                filename=log_dir + "/census2xlsx.log", filemode="w", level=tmpLevel
            )
            self.logger = logging.getLogger("Census2Xlsx")

            # add custom stream handler to print to terminal if verboseFlag is active
            if self.verboseFlag:
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(tmpLevel)
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "%H:%M:%S",
                )
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)

            self.logger.info("Initializing...")

        # load censusTables.json
        with open(data_dir + "/censusTables.json", "r") as loadfile:
            self.census_tables_file = json.load(loadfile)
        if self.logFlag:
            self.logger.info("Loaded censusTables.json")

        # load customTables.json
        with open(data_dir + "/customTables.json", "r") as loadfile:
            self.custom_tables_file = json.load(loadfile)
        if self.logFlag:
            self.logger.info("Loaded customTables.json")

        if self.logFlag:
            self.logger.info("Initialized successfully")

    def generate_tables(self, report_area, selected_tables, options):
        """
        generate_tables will download census_tables, calculate custom_tables, and output custom_tables to
            a .xlsx file
        :param report_area: A set of locations defined by geocodes
        :param selected_tables: A set of tables that need to be calculated and then saved
        """
        if self.logFlag:
            self.logger.info("Generating...")

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

        # for each table in selected_tables, add table indicators to list to be downloaded
        self.select_tables(selected_tables)

        # for each location in report_area, download the census data and store in census_tables
        for location in report_area:
            self.download_tables(location, census_tables)

        # calculated the selected tables and store in custom_tables
        # tmp is used for calculating custom_tables. It is removed at end of calculations
        custom_tables["tmp"] = ""
        self.calculate_tables(selected_tables, census_tables, custom_tables)
        del custom_tables["tmp"]

        # TODO: use or remove:
        # print(json.dumps(custom_tables, indent=4))

        # save custom_tables to .xlsx file defined by output_path
        workbook = xlsxwriter.Workbook(options["outputFile"])
        self.save_tables(workbook, census_tables, custom_tables)
        workbook.close()

        if self.logFlag:
            self.logger.info("Generated successfully")

    def select_tables(self, selected_tables):
        for table in selected_tables:
            for indicator in self.custom_tables_file[table["sectionIdx"]][
                "SectionTables"
            ][table["tableIdx"]]["TableIndicators"]:
                for item in indicator["IndicatorFormula"]:
                    if len(item) != 1 and item[0] != "!":
                        # Indicator ID into detailed_table_IDs
                        if item[0] == "B":
                            self.detailed_table_IDs.append(item)
                        # Indicator ID into subject_table_IDs
                        if item[0] == "S":
                            self.subject_table_IDs.append(item)
                        # Indicator ID into data_profile_IDs
                        if item[0] == "D":
                            self.data_profile_IDs.append(item)

    def download_tables(self, location, census_tables):
        """
        download_tables will download all tables for a single location and store it in census_tables
        :param location: The location to download
        :param census_tables: The dictionary to store the downloaded indicators
        """
        if self.logFlag:
            self.logger.info("Downloading...")

        # aquire the geocode for the location (location can be of any geographic level)
        geo_code = None
        if location["geographicLevel"] == "0":
            geo_code = censusdata.censusgeo([("state", location["primaryID"])])
        elif location["geographicLevel"] == "1":
            geo_code = censusdata.censusgeo(
                [
                    ("state", location["primaryID"]),
                    ("county", location["secondaryID"]),
                ]
            )
        elif location["geographicLevel"] == "2":
            geo_code = censusdata.censusgeo(
                [
                    ("state", location["primaryID"]),
                    ("place", location["secondaryID"]),
                ]
            )

        if geo_code:
            location_name = location["locationName"]
            census_tables[location_name] = {}

            # download Detailed Tables for the geo_code and add to census_tables
            if len(self.detailed_table_IDs) > 0:
                downloaded_data = censusdata.download(
                    self.census_type,
                    self.census_year,
                    geo_code,
                    self.detailed_table_IDs,
                )
                downloaded_data = downloaded_data.to_dict()
                dl_keys = list(downloaded_data.keys())
                for dl_key in dl_keys:
                    census_tables[location_name][dl_key] = downloaded_data[dl_key][
                        geo_code
                    ]

            # download Subject Tables for the geo_code and add to census_tables
            if len(self.subject_table_IDs) > 0:
                downloaded_data = censusdata.download(
                    self.census_type,
                    self.census_year,
                    geo_code,
                    self.subject_table_IDs,
                    tabletype="subject",
                )
                downloaded_data = downloaded_data.to_dict()
                dl_keys = list(downloaded_data.keys())
                for dl_key in dl_keys:
                    census_tables[location_name][dl_key] = downloaded_data[dl_key][
                        geo_code
                    ]

            # download Data Profile Tables for the geo_code and add to census_tables
            if len(self.data_profile_IDs) > 0:
                downloaded_data = censusdata.download(
                    self.census_type,
                    self.census_year,
                    geo_code,
                    self.data_profile_IDs,
                    tabletype="profile",
                )
                downloaded_data = downloaded_data.to_dict()
                dl_keys = list(downloaded_data.keys())
                for dl_key in dl_keys:
                    census_tables[location_name][dl_key] = downloaded_data[dl_key][
                        geo_code
                    ]
        else:
            if self.logFlag:
                self.logger.warning(
                    "Invalid location in report_area: %s", location["location_name"]
                )

        if self.logFlag:
            self.logger.info("Downloaded successfully")

    def calculate_formula(self, formula, location_name, census_tables, custom_tables):
        """
        calculate_formula calculates a specific indicator for a specific location and stores it in
            custom_tables. Uses a Reverse Polish notation (RPN) calculator.
        :param formula: a string showing how to calculate this specific indicator
        :param location_name: the location being calcculated
        :param census_tables: the dictionary containing Indicators to use in the calculation
        :param custom_tables: the dictionary storing the calculated Indicators
        """
        if self.logFlag and self.debugFlag:
            self.logger.debug("Formula: %a", formula)

        # create a "stack" for the RPN calculator
        calculator = []

        # for each item in the formula...
        for item in formula:
            # if the item is of length 1, it is an operator
            if len(item) == 1:
                # if the item is "s", save the top of the stack as a temporary variable
                if item == "s":
                    if custom_tables["tmp"] != "":
                        if self.logFlag:
                            self.logger.warning("Tried to overwrite the tmp variable")
                        sys.exit(2)
                    custom_tables["tmp"] = calculator[len(calculator) - 1]
                # if the item is "l", load the temporary variable to top of the stack
                if item == "l":
                    if custom_tables["tmp"] == "":
                        if self.logFlag:
                            self.logger.warning(
                                "Tried to load tmp variable but non exists"
                            )
                        sys.exit(2)
                    calculator.append(custom_tables["tmp"])
                    custom_tables["tmp"] = ""
                # if the item is "r", round the variable at the top of the stack
                if item == "r":
                    a = calculator.pop()
                    calculator.append(round(a, 2))
                # if the item is "%", pop 1 variable from the stack, then push the variable back with a % appended to the end
                if item == "%":
                    a = calculator.pop()
                    calculator.append(str(round(a, 2)) + "%")
                # if the item is "+", pop and add 2 variables from the stack, then push the result to the stack
                if item == "+":
                    b = calculator.pop()
                    a = calculator.pop()
                    calculator.append(a + b)
                # if the item is "-", pop and subtract 2 variables from the stack, then push the result to the stack
                if item == "-":
                    b = calculator.pop()
                    a = calculator.pop()
                    calculator.append(a - b)
                # if the item is a "*", pop and multiply 2 variables from the stack, then push the result to the stack
                if item == "*":
                    b = calculator.pop()
                    a = calculator.pop()
                    calculator.append(a * b)
                # if the item is "/", pop and divide 2 variables from the stack, then push the result to the stack
                if item == "/":
                    b = calculator.pop()
                    a = calculator.pop()
                    if b == 0:
                        if self.logFlag:
                            self.logger.warning("Tried to divide by zero")
                            self.logger.warning("%s / %s" % (str(a), str(b)))
                        if a == 0:
                            calculator.append(0)
                        else:
                            sys.exit(2)
                    else:
                        calculator.append(a / b)

            # if the item is greater than length 1, it is an operand or a literal
            else:
                # if the item starts with "!", it is a literal
                if item[0] == "!":
                    calculator.append(int(item.split(" ")[1]))
                # if the item does not start with "!", it is an operand
                else:
                    calculator.append(census_tables[location_name][item])

            if self.logFlag and self.debugFlag:
                self.logger.debug(calculator)
                if custom_tables["tmp"] != "":
                    self.logger.debug("tmp: %s" % str(custom_tables["tmp"]))

        return calculator.pop()

    def calculate_tables(self, selected_tables, census_tables, custom_tables):
        """
        calculate_tables calculates custom_tables from census_tables
        :param census_tables: the downloaded indicators from the census
        :param custom_tables: the dictionary to store the calculated indicators
        """
        if self.logFlag:
            self.logger.info("Calculating...")

        # for each table in selected_tables
        for table in selected_tables:
            section_name = self.custom_tables_file[table["sectionIdx"]]["SectionName"]
            if section_name not in custom_tables:
                custom_tables[section_name] = {}
            table_name = self.custom_tables_file[table["sectionIdx"]]["SectionTables"][
                table["tableIdx"]
            ]["TableName"]
            custom_tables[section_name][table_name] = {}
            indicators = self.custom_tables_file[table["sectionIdx"]]["SectionTables"][
                table["tableIdx"]
            ]["TableIndicators"]
            for location_name in list(census_tables.keys()):
                custom_tables[section_name][table_name][location_name] = {}
                for indicator in indicators:
                    indicator_name = indicator["IndicatorName"]
                    custom_tables[section_name][table_name][location_name][
                        indicator_name
                    ] = {}
                    if self.logFlag and self.debugFlag:
                        self.logger.debug(
                            "Calculating: %s - %s - %s - %s",
                            section_name,
                            table_name,
                            indicator_name,
                            location_name,
                        )

                    # calculate the indicator and store in custom_tables
                    custom_tables[section_name][table_name][location_name][
                        indicator_name
                    ] = self.calculate_formula(
                        indicator["IndicatorFormula"],
                        location_name,
                        census_tables,
                        custom_tables,
                    )

        if self.logFlag:
            self.logger.info("Calculated successfully")

    def save_tables(self, workbook, census_tables, custom_tables):
        """
        save_tables writes custom_tables to workbook
        :param workbook: an open .xlsx file to save the custom_tables
        :param custom_tables: the dictionary storing the calculated Indicators
        """
        if self.logFlag:
            self.logger.info("Saving...")

        # create custom formats for human readability
        table_format = workbook.add_format(
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
        indicator_format = workbook.add_format(
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
        location_format = workbook.add_format(
            {
                "font_name": "Times New Roman",
                "bold": False,
                "align": "left",
                "valign": "bottom",
                "text_wrap": False,
                "border": True,
            }
        )
        data_format = workbook.add_format(
            {
                "font_name": "Times New Roman",
                "bold": False,
                "align": "right",
                "valign": "bottom",
                "text_wrap": False,
                "border": True,
            }
        )

        # for each section in custom_tables...
        for section_name in list(custom_tables.keys()):
            # create a new worksheet for this section
            worksheet = workbook.add_worksheet(section_name)
            row = 0
            col = 0
            # for each table in the section...
            for table_name in list(custom_tables[section_name].keys()):
                indicators = list(
                    custom_tables[section_name][table_name][
                        list(census_tables.keys())[0]
                    ].keys()
                )
                # write a table header the width of the table
                worksheet.merge_range(
                    row,
                    0,
                    row,
                    len(indicators),
                    table_name,
                    table_format,
                )
                row += 1
                # write "Report Area" on the indicator line
                worksheet.write(row, col, "Report Area", indicator_format)
                col += 1
                # for each indicator in the table...
                for indicator_name in indicators:
                    # write the indicator on the indicator line
                    worksheet.write(row, col, indicator_name, indicator_format)
                    col += 1
                row += 1
                col = 0
                # for each location in the report_area...
                for location_name in list(census_tables.keys()):
                    # write the location name on a new line
                    worksheet.write(row, col, location_name, location_format)
                    col += 1
                    for indicator_name in indicators:
                        indicator = custom_tables[section_name][table_name][
                            location_name
                        ][indicator_name]
                        # write the indicator data to the respective table cell
                        worksheet.write(row, col, indicator, data_format)
                        col += 1
                    row += 1
                    col = 0
                row += 1

        if self.logFlag:
            self.logger.info("Saved successfully")


def main(data_dir, log_dir=""):
    """
    This function is not intended as main entry point for the Census2Xlsx class. Normally, users
    will create report_area and selected_indicators via the GUI. Thus, a hard-coded report_area and
    selected_indicators is used here for debugging purposes.
    """

    # create an instance of the Census2Xlsx class
    c2x = Census2Xlsx(data_dir, log_dir)

    # create a test report_area
    report_area = [
        {
            "locationName": "Alabama",
            "geographicLevel": "0",
            "primaryID": "01",
            "secondaryID": "-1",
        },
        # {
        #     "locationName": "Autauga County, Alabama",
        #     "geographicLevel": "1",
        #     "primaryID": "01",
        #     "secondaryID": "001",
        # },
        # {
        #     "locationName": "Abanda, Alabama",
        #     "geographicLevel": "2",
        #     "primaryID": "01",
        #     "secondaryID": "00100",
        # },
    ]

    # create a test selected_indicators
    selected_indicators = [
        {"sectionIdx": 0, "tableIdx": 0},
        # {"sectionIdx": 0, "tableIdx": 1},
        # {"sectionIdx": 0, "tableIdx": 2},
        # {"sectionIdx": 0, "tableIdx": 3},
        # {"sectionIdx": 0, "tableIdx": 4},
        # {"sectionIdx": 0, "tableIdx": 5},
        # {"sectionIdx": 0, "tableIdx": 6},
        # {"sectionIdx": 0, "tableIdx": 7},
        # {"sectionIdx": 0, "tableIdx": 8},
        # {"sectionIdx": 0, "tableIdx": 9},
        # {"sectionIdx": 0, "tableIdx": 10},
        # {"sectionIdx": 1, "tableIdx": 0},
        # {"sectionIdx": 1, "tableIdx": 1},
        # {"sectionIdx": 1, "tableIdx": 2},
        # {"sectionIdx": 1, "tableIdx": 3},
        # {"sectionIdx": 1, "tableIdx": 4},
        # {"sectionIdx": 1, "tableIdx": 5},
        # {"sectionIdx": 1, "tableIdx": 6},
        # {"sectionIdx": 1, "tableIdx": 7},
        # {"sectionIdx": 2, "tableIdx": 0},
        # {"sectionIdx": 2, "tableIdx": 1},
        # {"sectionIdx": 2, "tableIdx": 2},
        # {"sectionIdx": 2, "tableIdx": 3},
        # {"sectionIdx": 2, "tableIdx": 4},
        {"sectionIdx": 2, "tableIdx": 5},
    ]

    # create test options
    options = {"outputPath": "./output/test.xlsx"}

    # run the Census2Xlsx generate_tables method
    c2x.generate_tables(report_area, selected_indicators, options)


def usage():
    print("census2xlsx.py -d <data_directory> -l <log_directory> -o <output_directory>")


if __name__ == "__main__":
    # default directories
    DATA_DIR = "./src/assets/data"
    LOG_DIR = "./logs"

    # process command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:l:", ["help", "ddir=", "ldir="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt in "-d":
            DAT_DIR = arg
        elif opt in "-l":
            LOG_DIR = arg

    main(DATA_DIR, LOG_DIR)
