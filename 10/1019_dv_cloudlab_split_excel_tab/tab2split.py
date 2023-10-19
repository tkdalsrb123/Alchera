import os, sys, logging
import pandas as pd
from collections import defaultdict

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
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

excel_dict = readfiles(input_dir, '.xlsx')
error_file = []
for filename, excel_path in excel_dict.items():
    logger.info(excel_path)
    try:
        xls = pd.ExcelFile(excel_path)
        for sheet_name in xls.sheet_names:
            output_excel_path = os.path.join(output_dir, f"{sheet_name}.xlsx")
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            df.to_excel(output_excel_path, index=False)
    except:
        error_file.append(excel_path)
        print(excel_path)

error = pd.DataFrame(error_file, columns=['error_path'])        
error.to_excel(f'./error_list.xlsx', index=False)