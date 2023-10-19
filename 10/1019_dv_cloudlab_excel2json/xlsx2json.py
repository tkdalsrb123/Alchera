import os, sys, json, logging
import pandas as pd
import numpy as np
from collections import defaultdict
from tqdm import tqdm
tqdm.pandas()

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

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_folder = os.path.join(output_dir, mid_dir, filename)
    os.makedirs(output_folder, exist_ok=True)

    return output_folder


def saveJson(file, path):
    with open(path, 'w') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)

def if_nan(t):
    if t == np.NAN:
        return ""
    else:
        return t


def jsonTree(x):
    a = x.iloc[0]
    b = x.iloc[1]
    c = x.iloc[2]
    d = x.iloc[3]
    e = x.iloc[4]
    f = x.iloc[5]
    g = x.iloc[6]
    h = x.iloc[7]
    i = x.iloc[8]
    if np.NAN in [a, c, d, e, g, h]:
        error_list.append(a)
        return
    else:    
        b = if_nan(b)
        f = if_nan(f)
        i = if_nan(i)
            
        tree = {
            "ojects": {
                "contents": [
                {
                    "Value.ID": a,
                    "Value.WBS": b,
                    "Value.TYPE": c 
                },
                {
                    "Value.CAUSE": d,
                    "CAUSE.Keyword1": e,
                    "CAUSE.Keyword2": f
                },
                {
                    "Value.COUNTERMEASURE": g,
                    "COUNTERMEASURE.Keyword1": h,
                    "COUNTERMEASURE.Keyword2": i
                }
            ]
        }
        }

        if copy == a:
            if os.path.isfile(f'{output_folder}/{copy}.json'):
                os.rename(f'{output_folder}/{copy}.json', f'{output_folder}/{copy}_1.json')
                num = 2
            else:
                saveJson(tree, f'{output_folder}/{a}_{num}.json')
                num += 1
            
        else:
            saveJson(tree, f'{output_folder}/{a}.json')
            
        copy = a

        
if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    excel_dict = readfiles(input_dir, '.xlsx')
    error_list = []
    for filename, excel_path in tqdm(excel_dict.items(), desc='전체 excelfile', position=0):
        logger.info(excel_path)
        output_folder = makeOutputPath(excel_path, input_dir, output_dir)
        excel = pd.read_excel(excel_path)
        # excel.progress_apply(jsonTree, axis=1)
        copy = ""
        for i in range(excel.shape[0]):
            x = excel.loc[i]
            a = x.iloc[0]
            b = x.iloc[1]
            c = x.iloc[2]
            d = x.iloc[3]
            e = x.iloc[4]
            f = x.iloc[5]
            g = x.iloc[6]
            h = x.iloc[7]
            i = x.iloc[8]
            logger.info(a)
            if np.NAN in [a, c, d, e, g, h]:
                error_list.append(a)
            else:    
                b = if_nan(b)
                f = if_nan(f)
                i = if_nan(i)
                    
                tree = {
                    "ojects": {
                        "contents": [
                        {
                            "Value.ID": a,
                            "Value.WBS": b,
                            "Value.TYPE": c 
                        },
                        {
                            "Value.CAUSE": d,
                            "CAUSE.Keyword1": e,
                            "CAUSE.Keyword2": f
                        },
                        {
                            "Value.COUNTERMEASURE": g,
                            "COUNTERMEASURE.Keyword1": h,
                            "COUNTERMEASURE.Keyword2": i
                        }
                    ]
                }
                }

                if copy == a:
                    if os.path.isfile(f'{output_folder}/{copy}.json'):
                        os.rename(f'{output_folder}/{copy}.json', f'{output_folder}/{copy}_1.json')
                        saveJson(tree, f'{output_folder}/{copy}_2.json')
                        num = 3
                    else:
                        saveJson(tree, f'{output_folder}/{copy}_{num}.json')
                        num += 1
                    
                else:
                    saveJson(tree, f'{output_folder}/{a}.json')
                    
                copy = a


    df = pd.DataFrame(error_list, columns=['error_name'])
    df.to_excel(f'{output_dir}/error_list.xlsx', index=False)