import os, sys, json
from collections import defaultdict

def readfiles(dir, Ext):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_list.append(file_path)
    return file_list

_, input_dir, output_dir = sys.argv

json_list = readfiles(input_dir, '.json')

for json_path in json_list:
    
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    print(json_file)