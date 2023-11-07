import os, sys, json
import pandas as pd
from collections import defaultdict

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

def readJson(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    json_dict = readfiles(input_dir, '.json')

    list2df = []
    for filename, json_path in json_dict.items():
        
        data = readJson(json_path)
        
        val_list = [filename]
        if 'FW' in filename:
            val = data['Favorite word']
            [val_list.append(' '.join(v)) for v in val]
        elif 'PF' in filename:
            val = data['Preferred Form']
            [val_list.append(' '.join(v)) for v in val.values()]
        else:
            val = data['behavioral pattern']  
            [val_list.append(' '.join(v)) for v in val.values()]
        
        list2df.append(val_list)

    df = pd.DataFrame(list2df)
    df.to_excel(f"{output_dir}/json_results.xlsx", index=False, header=None)
    