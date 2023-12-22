import os, sys, json, logging
import pandas as pd
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
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def make_csv(_list, col, output_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_csv(output_path, index=False)
    
def get_true_value(values):
    for value in values:
        if value['selected'] == True:
            val = value['value']
    return val

if __name__ == "__main__":
    _, input_dir = sys.argv
    
    folder_front_list = [os.path.join(input_dir, dirs, '04-1_Lane_grouping', '1_Front') for dirs in os.listdir(input_dir)]
    folder_side_list = [os.path.join(input_dir, dirs, '04-1_Lane_grouping', '2_Side') for dirs in os.listdir(input_dir)]
    
    file_dict = defaultdict(lambda : defaultdict(list))
    for folder in tqdm(folder_front_list, desc='gather file'):
        seq = folder.split('\\')[-3]
        file_dict[seq]['1_Front'] = [(os.path.join(folder, file)) for file in os.listdir(folder)]

    for folder in tqdm(folder_side_list, desc='gather file'):
        seq = folder.split('\\')[-3]
        file_dict[seq]['2_Side'] = [(os.path.join(folder, file)) for file in os.listdir(folder)]
        

    list2df = []
    for seq, json_path_dict in tqdm(file_dict.items(), desc='create csv'):
        info_dict = {"0_Unknown":0, "1_None":0, "2_Solid":0, "3_Dashed":0, "4_Double_Solid":0, "5_Double_Dashed":0, "6_1st-Dashed&2nd-Solid":0, "7_1st-Solid&2nd-Dashed":0}

        for direc, json_path_list in json_path_dict.items():
            for json_path in json_path_list:
                data = readJson(json_path)
                if len(data['objects']) == 2:
                    for obj in data['objects']:
                        for att in obj['attributes']:
                            val = get_true_value(att['values'])
                        info_dict[val] += 1
                elif len(data['objects']) == 1:
                    info_dict['1_None'] += 1
                    for obj in data['objects']:
                        for att in obj['attributes']:
                            val = get_true_value(att['values'])
                elif len(data['objects']) == 0:
                    info_dict['1_None'] += 2
      
            list2df.append([seq, direc, info_dict["0_Unknown"], info_dict["1_None"], info_dict["2_Solid"], info_dict["3_Dashed"], info_dict["4_Double_Solid"], info_dict["5_Double_Dashed"], info_dict["6_1st-Dashed&2nd-Solid"], info_dict["7_1st-Solid&2nd-Dashed"]])
    
    make_csv(list2df, ["sequence", 'View', "0_Unknown", "1_None", "2_Solid", "3_Dashed", "4_Double_Solid", "5_Double_Dashed", "6_1st-Dashed&2nd-Solid", "7_1st-Solid&2nd-Dashed"], f'./{os.path.split(input_dir)[-1]}.csv')

