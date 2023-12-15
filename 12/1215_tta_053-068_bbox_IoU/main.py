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

def IoU(box1, box2):
    # box = (x1, y1, x2, y2)
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # obtain x1, y1, x2, y2 of the intersection
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # compute the width and height of the intersection
    w = max(0, x2 - x1 + 1)
    h = max(0, y2 - y1 + 1)

    inter = w * h
    iou = inter / (box1_area + box2_area - inter)
    return iou

if __name__ == '__main__':
    _, label_dir, treeD_dir = sys.argv
    
    logger = make_logger('log.log')
    label_dict = readfiles(label_dir, '.json')
    treeD_dict = readfiles(treeD_dir, '.json')
    
    list2df = []
    for filename, label_path in tqdm(label_dict.items()):
        treeD_path = treeD_dict.get(filename)
        logger.info(treeD_path)
        if treeD_path: 
            label_data = readJson(label_path)
            treeD_data = readJson(treeD_path)
            
            label_list = []
            for ann in label_data['annotations']:
                coor = ann['bbox']
                if len(coor) == 4:
                    x1 = coor[0]
                    y1 = coor[1]
                    x2 = coor[2]
                    y2 = coor[3]
                    label_list.append((x1, y1, x2, y2))
            
            treeD_list = []
            for obj in treeD_data['objects']:
                if obj['name'] == '영역오류':
                    x1 = obj['points'][0][0]
                    y1 = obj['points'][0][1]
                    x2 = obj['points'][1][0]
                    y2 = obj['points'][1][1]
                    treeD_list.append((x1,y1,x2,y2))
                    

            for treeD in treeD_list:
                iou_list = []
                for label in label_list:
                    iou = IoU(treeD, label)
                    iou_list.append(iou)

                max_iou = max(iou_list)
                list2df.append([filename, max_iou])
        
    df = pd.DataFrame(list2df, columns=['파일명', 'IoU값'])
    df.to_excel(f"./IoU.xlsx", index=False)