import os, sys, logging, shutil
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

def readfiles(dir):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if "WIN" not in filename:
                unique = filename[:9] + filename[-13:]
            else:
                unique = filename[:13] + filename[-13:]
                
            file_path = os.path.join(root, file)
        
            file_dict[unique].append(file_path)
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
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    file_dict = readfiles(input_dir)
    
    for unique, file_path_list in tqdm(file_dict.items()):
        for file_path in file_path_list:
            logger.info(file_path)
            folder = os.path.join(output_dir, unique)
            os.makedirs(folder, exist_ok=True)
            file = os.path.split(file_path)[-1]
            output_path = os.path.join(folder, file)

            shutil.copy2(file_path, output_path)