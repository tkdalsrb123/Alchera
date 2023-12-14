import os, sys, logging
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
tqdm.pandas()

try:
    import tensorflow
except:
    os.system("pip install tensorflow")

try:
    from pykospacing import Spacing
except:
    os.system("pip install git+https://github.com/haven-jeon/PyKoSpacing.git")
    from pykospacing import Spacing
    
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

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def spacing_preprocessing(x):
    CAUSE = x.iloc[1]
    TYPE = x.iloc[4]
    COUNTER = x.iloc[5]

    x.iloc[3] = spacing(CAUSE)
    x.iloc[4] = spacing(TYPE)
    x.iloc[5] = spacing(COUNTER)

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    excel_dict = readfiles(input_dir, '.xlsx')

    spacing=Spacing()

    for filename, excel_path in tqdm(excel_dict.items(), desc='all excel'):
        logger.info(excel_path)
        output_xlsx_path = makeOutputPath(excel_path, input_dir, output_dir, 'xlsx')
        excel = pd.read_excel(excel_path)

        excel.progress_apply(spacing_preprocessing, axis=1)
        
        excel.to_excel(output_xlsx_path, index=False)
