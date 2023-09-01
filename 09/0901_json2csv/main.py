import os, sys, json
import pandas as pd
from tqdm import tqdm 
import logging

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
    file_list =[]
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)
                file_list.append(file_path)

    return file_list

def makedf(li, col_name):
    df = pd.DataFrame(li, columns=col_name)
    return df

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_list = readfiles(input_dir)

for json_path in tqdm(json_list):
    logger.info(json_path)
    root, file = os.path.split(json_path)
    filename, ext = os.path.splitext(file)
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_csv_path = os.path.join(folder, f"{filename}.csv")
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)

    meta = json_file['meta']
    meta = [[k,v] for k, v in meta.items() if k != 'tester_id']
    
    q_list = []
    a_list = []
    g_list = []
    c_list = []
    q_list.append(json_file['comment']['question'])
    g_list.append(json_file['comment']['grade'])
    c_list.append(json_file['comment']['comment'])
    for comment_key, comment_val in json_file['comment'].items():
        if "answer" in comment_key:
            a_list.append(comment_val)
    
    meta_df = makedf(meta, ['meta_key', 'meta_value'])
    q_df = makedf(q_list, ['question'])
    a_df = makedf(a_list, ['answer'])
    g_df = makedf(g_list, ['grade'])
    c_df = makedf(c_list, ['comment'])
    outer_df = meta_df.merge(q_df, how='outer', left_index=True, right_index=True)
    outer_df = outer_df.merge(a_df, how='outer', left_index=True, right_index=True)
    outer_df = outer_df.merge(g_df, how='outer', left_index=True, right_index=True)
    outer_df = outer_df.merge(c_df, how='outer', left_index=True, right_index=True)
    outer_df.to_csv(output_csv_path, encoding='utf-8', index=False)