import os, sys, logging, shutil
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

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

def make_xlsx(_list):
    df = pd.DataFrame(_list, columns=['filename'])
    df.to_excel('./error_file.xlsx', index=False)

if __name__ == "__main__":
    _, excel_dir, input_dir, output_dir = sys.argv

    logger = make_logger('log.log')
    file_list = []
    df = pd.read_excel(excel_dir)
    
    df['추가할 파일'].apply(lambda x: file_list.append(os.path.splitext(x)[0]))
    file_dict = readfiles(input_dir, '.png')
    error_list = []
    for file_name in tqdm(file_list):
        logger.info(file_name)
        file_path = file_dict.get(file_name)
        if file_path:
            file = os.path.split(file_path)[-1]
            output_path = os.path.join(output_dir, file)
            shutil.copy2(file_path, output_path)
        else:
            error_list.append(file_name)
    
    make_xlsx(error_list)