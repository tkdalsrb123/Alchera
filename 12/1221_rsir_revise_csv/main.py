import os, sys, logging
import pandas as pd
from tqdm import tqdm
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
                
                break
            
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

if __name__ == "__main__":
    _, input_dir = sys.argv
    logger = make_logger('log.log')    
    csv_dict = readfiles(input_dir, '.csv')


    for filename, csv_path in tqdm(csv_dict.items()):
        logger.info(csv_path)
        output_txt_path = os.path.splitext(csv_path)[0] + '.txt'
        df = pd.read_csv(csv_path)

        new_df = df[['Timestamp(s)_CLU11', 'VehicleSpeed(km/h)', 'VehicleYawRate(deg/x)', 'pitch']]

        new_df.columns = ['timestamp', 'whl_spd', 'yaw_rate', 'pitch_rate']
        new_df.to_string(output_txt_path, index=False)
        
        
        