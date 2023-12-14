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

def is_nan(val):
    if type(val) != float:
        return val
    else:
        return ""
def spacing_preprocessing(x):
    col = ["정제_원인 문장", "정제_재해 유형", "정제_대책 문장"]
    # CAUSE = x.iloc[1]
    # TYPE = x.iloc[2]
    # COUNTER = x.iloc[3]

    # x.iloc[1] = spacing(CAUSE)
    # x.iloc[2] = spacing(TYPE)
    # x.iloc[3] = spacing(COUNTER)
    col0 = is_nan(x[col[0]])
    col1 = is_nan(x[col[1]])
    col2 = is_nan(x[col[2]])
    
    
    x[col[0]] = spacing(col0)
    x[col[1]] = spacing(col1)
    x[col[2]] = spacing(col2)

    return x

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    excel_dict = readfiles(input_dir, '.xlsx')

    spacing=Spacing()

    for filename, excel_path in tqdm(excel_dict.items(), desc='all excel', position=0):
        logger.info(excel_path)
        output_xlsx_path = makeOutputPath(excel_path, input_dir, output_dir, 'xlsx')
        excel = pd.read_excel(excel_path)

        for index, row in tqdm(excel.iterrows(), total=excel.shape[0], desc='filename', position=1):
            modified_row = spacing_preprocessing(row)
            excel.at[index] = modified_row
        
        excel.to_excel(output_xlsx_path, index=False)
