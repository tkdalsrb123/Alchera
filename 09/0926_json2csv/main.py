import os, sys, json
import pandas as pd

def readfiles(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename ,ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)

                file_list.append(file_path)
    return file_list

_, input_dir, output_dir = sys.argv

json_list = readfiles(input_dir)

df2list = []
for json_path in json_list:
    root, file = os.path.split(json_path)
    with open(json_path, encoding='utf-8-sig') as f:
        json_file = json.load(f)
    obj_points = None
    sha_points = None
    con_2_points = None
    con_points = None
    for json_info in json_file:
    # if type(json_file['objects']) == list:
        for obj in json_info['objects']:
            name = obj['name']
            if  name == "Object_segmentation":
                obj_points = obj['points']
            elif name == "Shadow_segmentation":
                sha_points = obj['points']
            
            elif name == "contact_line_2":
                con_2_points = obj['points']
            
            elif name == "contact_line":
                con_points = obj['points']
            
    # elif type(json_file['objects']) == dict:
    #     name = json_file['objects']['name']
    #     obj_points = None
    #     sha_points = None
    #     con_2_points = None
    #     con_points = None
    #     if 'Object' in name:
    #         obj_points = json_file['objects']['points']
        
    #     elif 'Shadow' in name:
    #         sha_points = json_file['objects']['points']
        
    #     elif '2' in name:
    #         con_2_points = json_file['objects']['points']
        
    #     elif 'contact' in name:
    #         con_points = json_file['objects']['points']
        
        
    df2list.append([file, obj_points, sha_points, con_points, con_2_points])

df = pd.DataFrame(df2list, columns=['filename', 'Object_segmentation', 'Shadow_segmentation', 'contact_lin', 'contact_line_2'])
df.to_csv(f"{output_dir}/seg_points.csv", encoding='utf-8', index=False)
