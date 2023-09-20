import os, sys
import pandas as pd
import logging
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

_, input_dir, csv_dir = sys.argv

logger = make_logger('log.log')
# csv file
info_dict = defaultdict(dict)
df = pd.read_csv(csv_dir, encoding='cp949')
df.apply(lambda x: info_dict.update({x['이름']: ''.join([str(x['ID']).zfill(3), str(x['나이']), str(x['성별'])])}), axis=1)

# read all img
img_dict = defaultdict(list)
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.jpg' or ext == '.dng':
            img_path = os.path.join(root, file)
            name = os.path.split(root)[-1]
            
            img_dict[name].append(img_path)

# rename filename
for name, img_path in tqdm(img_dict.items()):
    add_filename = info_dict[name]
    for path in img_path:
        logger.info(path)
        root, file = os.path.split(path)
        filename, ext = os.path.splitext(file)
        filename = f'{add_filename}_{filename}{ext}'
        new_name = os.path.join(root, filename)
        os.rename(path, new_name)
    