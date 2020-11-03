import censusdata
import json
import xlsxwriter
from tools import printTableCheck
import logging

"""
Author: Charles Herrmann
Date: 9/28/20
Description: A class for quickly gathering community needs assessment data for a specific geographic level in the US

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

# Comment out the following line if this isn't the entry file of if you don't want logging
logging.basicConfig(filename='c2x.log', filemode='w', level=logging.INFO)


class CensusModel:
    censusType = 'acs5'
    censusYear = 2018
    censusTables = None
    dataTableDesc = None
    geographies = None
    logger = logging.getLogger('model')

    def __init__(self):
        self.logger.info('initializing...')

        # load censusTables.json
        with open('censusTables.json', 'r') as loadfile:
            self.censusTables = json.load(loadfile)
        self.logger.info('loaded censusTables.json')

        # load dataTableDescriptions.json
        with open('dataTableDescriptions.json', 'r') as loadfile:
            self.dataTableDesc = json.load(loadfile)
        self.logger.info('loaded dataTableDescriptions.json')

        # load geographies.json
        with open('geographies.json', 'r') as loadfile:
            self.geographies = json.load(loadfile)
        self.logger.info('loaded geographies.json')

        self.logger.info('initialized successfully')

    def genData(self, geos, tables, fileName):
        self.logger.info('generating...')

        # data holds all the raw data collected from the census
        data = {}
        # dataTables holds the edited data calculated from the data dictionary
        dataTables = {}

        # loop through report area locations and obtain all required data from census
        for key in geos.keys():
            if geos[key]['selected']:
                # select geography
                geo = censusdata.geographies(censusdata.censusgeo([('state', geos[key]['ID'])]), self.censusType,
                                             self.censusYear)

                # download census data from selected geography and cached tableIDs
                self.downloadData(data, geo, self.censusTables)

        # calculated desired dataTables
        # tmp is used for calculating dataTables. Will be removed at end of calculations
        dataTables['tmp'] = ''
        self.calculateData(data, dataTables)
        del dataTables['tmp']

        # save dataTables to xlsx file
        workbook = xlsxwriter.Workbook(fileName)
        self.saveData(workbook, dataTables)
        workbook.close()

        self.logger.info('generated successfully')

    def downloadData(self, data, geo, censusTables):
        self.logger.info('downloading...')
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
            dl = censusdata.download(self.censusType, self.censusYear, geo[g], all_TableIDs)
            dl = dl.to_dict()
            dl_keys = list(dl.keys())
            for dl_key in dl_keys:
                data[g][dl_key] = dl[dl_key][geo[g]]

        self.logger.info('downloaded successfully')

    def calculateFormula(self, formula, geo, data, dataTables):
        calculator = []
        for item in formula:
            if len(item) == 1:
                if item == 's':
                    if dataTables['tmp'] != '':
                        self.logger.warning('Tried to overwrite the tmp variable')
                        exit(1)
                    dataTables['tmp'] = calculator[len(calculator) - 1]
                    # print('=s=', dataTables['tmp'])
                if item == 'l':
                    # print('=l=', dataTables['tmp'])
                    if dataTables['tmp'] == '':
                        self.logger.warning('Tried to load tmp variable but non exists')
                        exit(1)
                    calculator.append(dataTables['tmp'])
                    dataTables['tmp'] = ''
                if item == '+':
                    b = calculator.pop()
                    a = calculator.pop()
                    calculator.append(a + b)
                if item == '-':
                    b = calculator.pop()
                    a = calculator.pop()
                    calculator.append(a - b)
                if item == '/':
                    b = calculator.pop()
                    a = calculator.pop()
                    if b == 0:
                        self.logger.warning('Divide non-zero by zero')
                        self.logger.warning(str(a) + ' / ' + str(b))
                        if a == 0:
                            calculator.append(0)
                    else:
                        calculator.append(a / b)
            else:
                if item[0] == '!':
                    calculator.append(int(item.split(' ')[1]))
                else:
                    calculator.append(data[geo][item])
            self.logger.debug(calculator)
            if dataTables['tmp'] != '':
                self.logger.debug('tmp:' + str(dataTables['tmp']))
        return calculator.pop()

    def calculateData(self, data, dataTables):
        self.logger.info('calculating...')
        data_keys = list(data.keys())
        dtDesc_keys = list(self.dataTableDesc.keys())
        for dtDesc_key in dtDesc_keys:
            if len(self.dataTableDesc[dtDesc_key]) > 0:
                dataTables[dtDesc_key] = {}
                dtDesc_labels = list(self.dataTableDesc[dtDesc_key].keys())
                for data_key in data_keys:
                    dataTables[dtDesc_key][data_key] = {}
                    for dtDesc_label in dtDesc_labels:
                        self.logger.debug('Model calculating ' + dtDesc_key + '-' + data_key + '-' + dtDesc_label)
                        dataTables[dtDesc_key][data_key][dtDesc_label] = self.calculateFormula(self.dataTableDesc[dtDesc_key][dtDesc_label], data_key, data, dataTables)

        self.logger.info('calculated successfully')

    def saveData(self, workbook, dataTables):
        self.logger.info('saving...')
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
            worksheet.write(row, col, 'Report Area', LabelFormat)
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
        self.logger.info('saved successfully')


# This main function was developed to test the CensusModel class.
# This function contains almost the exact code found in CensusModel.genData()
# The only modification is hard-coded geos and dataTables for debugging.
def main():
    cmodel = CensusModel()
    data = {}

    # Acquire geography
    tmp_geo = censusdata.geographies(censusdata.censusgeo([('zip code tabulation area', '11693')]), cmodel.censusType, cmodel.censusYear)
    # download census data from selected geography and cached tableIDs
    cmodel.downloadData(data, tmp_geo, cmodel.censusTables)

    """ vvv ALL ADDITIONAL GEOS IN THIS SECTION vvv """
    tmp_geo = censusdata.geographies(censusdata.censusgeo([('state', '36'), ('county', '081')]), cmodel.censusType, cmodel.censusYear)
    cmodel.downloadData(data, tmp_geo, cmodel.censusTables)
    tmp_geo = censusdata.geographies(censusdata.censusgeo([('state', '36')]), cmodel.censusType, cmodel.censusYear)
    cmodel.downloadData(data, tmp_geo, cmodel.censusTables)
    """ ^^^ ALL ADDITIONAL GEOS IN THIS SECTION ^^^ """

    # calculated desired dataTables
    dataTables = {'tmp': ''}  # tmp is used for calculating dataTables. Will be removed at end of calculations
    cmodel.calculateData(data, dataTables)
    del dataTables['tmp']

    # save dataTables to xlsx file
    workbook = xlsxwriter.Workbook('output.xlsx')
    cmodel.saveData(workbook, dataTables)
    workbook.close()


if __name__ == '__main__':
    main()

    """ The code below is for quickly searching geographies available in the census (comment out main if using) """
    # geos = censusdata.geographies(censusdata.censusgeo([('state', '36'), ('county', '*')]), 'acs5', 2018)
    # g_keys = list(geos.keys())
    # g_keys.sort()
    # for key in g_keys:
    #     print(key, '-', geos[key])
