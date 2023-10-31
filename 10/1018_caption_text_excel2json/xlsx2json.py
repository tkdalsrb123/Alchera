import os, sys, json, logging
import numpy as np
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
tqdm.pandas()

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

def jsonTree(x):
    b = str(x.iloc[1])
    c = str(x.iloc[2])
    d = str(x.iloc[3])
    e = str(x.iloc[4])
    f = x.iloc[5]
    a = str(x.iloc[0])
    if type(f) == float:
        error_list.append(a)
    tree = {'ojects': {
        "caption": [
            {
                "outline": "개요(제목)",
                "text": b
            },
            {
                "additional": "세부내용(외부항목-부가설명)",
                "text": c
            },
            {
                "contents": "세부내용(내부항목-그래프수치설명)",
                "text": d
            },
            {
                "summary": "그래프 요약(큰 흐름)",
                "text": e
            },
            {   
                "DataAccuracy":"정확도",
                "text": f
            }
        ]
    },
        "info": {
            "imageName": a
        }
    }
    
    filename = a.split('.')[0]
    saveJson(tree, f'{output_folder}/{filename}.json')
    
if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    excel_dict = readfiles(input_dir, '.xlsx')
    error_list = []
    for filename, excel_path in tqdm(excel_dict.items(), desc='전체 excelfile', position=0):
        output_folder = makeOutputPath(excel_path, input_dir, output_dir)
        excel = pd.read_excel(excel_path)

        excel.progress_apply(jsonTree, axis=1)

    df= pd.DataFrame(error_list, columns=['error file'])
    df.to_excel(f'{output_dir}/error_list.xlsx', index=False)