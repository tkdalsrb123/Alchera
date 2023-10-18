import os, sys, json, logging
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


def saveJson(file, path):
    with open(path, 'w') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)

def jsonTree(x):
    b = x.iloc[1]
    c = x.iloc[2]
    d = x.iloc[3]
    e = x.iloc[4]
    a = x.iloc[0]
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
            }
        ]
    },
        "info": {
            "imageName": a
        }
    }
    
    filename = a.split('.')[0]
    saveJson(tree, f'{output_dir}/{filename}.json')
    
if __name__ == '__main__':
    _, excel_dir, output_dir = sys.argv
    
    excel = pd.read_excel(excel_dir)

    excel.progress_apply(jsonTree, axis=1)