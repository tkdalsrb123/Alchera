import json, os, sys
import pandas as pd

def readfiles(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)
                file_list.append(file_path)
            
    return file_list


_, input_dir, output_dir = sys.argv

json_list = readfiles(input_dir)

df2list = []
for json_path in json_list:
    root, file = os.path.split(json_path)
    
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    
    bbox = json_file.get('bbox')
    polygon = json_file.get('polygon')
    
    if bbox:
        for code in bbox['mid_vienna_codes']:
            df2list.append([file, 'bbox', code, bbox['points']])
        
    if polygon:
        for code in polygon['mid_vienna_codes']:
            df2list.append([file, 'polygon', code, polygon['points']])
            
df = pd.DataFrame(df2list, columns=['파일명', 'box or polygon', 'mid_vienna_codes', 'point'])
df.to_excel(f'{output_dir}/count_list.xlsx', index=False)