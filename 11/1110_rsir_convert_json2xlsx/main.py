import os, sys, json, logging
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.datavalidation import DataValidation

def create_Excel(data, path):
    # Create a sample dataframe
    df = pd.DataFrame(data, columns=['No.', 'Source', 'Location', 'RoadType', 'IlluminationCondition'])

    # Write the dataframe to an Excel file
    excel_file = path
    df.to_excel(excel_file, index=False)

    # Open the workbook and select the active sheet
    wb = Workbook()
    ws = wb.active

    # Add the existing data from the dataframe to the Excel file
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Create a data validation drop-down list for the 'Category' column
    dl = DataValidation(type="list", formula1='"D_Road,D_Expressway,D_Hightway,D_OtherRoads"', allow_blank=True)
    dr = DataValidation(type="list", formula1='"General, TG, IC_JC, Tunnel, RoadConstruction, Intersection"', allow_blank=True)
    di = DataValidation(type="list", formula1='"Normal, DirectSunlight, DirectHeadLight, DirectStreetLight, VeryLowLight"', allow_blank=True)

    ws.add_data_validation(dl)
    ws.add_data_validation(dr)
    ws.add_data_validation(di)

    # Apply the data validation to the desired column
    for row in range(2, len(df) + 2):
        dl.add(f'C{row}')
        dr.add(f"D{row}")
        di.add(f"E{row}")
        
    # Save the workbook
    wb.save(excel_file)
    logger.info(excel_file)
    
def make_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # formatter
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s:%(lineno)d] -- %(message)s")
    # file_handler
    file_handler = logging.FileHandler(log, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    # logger.add
    logger.addHandler(file_handler)
    
    return logger

def readfiles(dir, Ext):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext and 'Property' in filename:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv

    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')    

    for filename, json_path in tqdm(json_dict.items()):
        output_excel_path = f"{output_dir}/{filename}.xlsx"
        logger.info(json_path)
        data = readJson(json_path)
        
        info_list = []
        for idx, info in enumerate(data):
            jpg_name = info['Source']
            location = info['Location']
            roadtype = info['RoadType']
            ill = info['IlluminationCondition']

            info_list.append([idx, jpg_name, location, roadtype, ill])
            
        create_Excel(info_list, output_excel_path)