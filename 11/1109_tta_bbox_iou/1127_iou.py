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
    _, label_dir, treeD_dir, output_dir = sys.argv
    
    label_dict = readfiles(label_dir, '.json')
    treeD_dict = readfiles(treeD_dir, '.json')
    
    list2df = []
    for filename, label_path in tqdm(label_dict.items()):
        treeD_path = treeD_dict.get(filename)
        if treeD_path:

            label_data = readJson(label_path)
            treeD_data = readJson(treeD_path)
            
            label_list = []
            bbox = label_data['bboxdata']["bbox_location"]
            bbox = [float(i) for i in bbox.split(',')]
            # x1 = round(bbox[0])
            # y1 = round(bbox[1])
            # x2 = round(bbox[2])
            # y2 = round(bbox[3])
            # label_list.append((x1, y1, x2, y2))
            
            treeD_list = []
            # for obj in treeD_data['objects']:
            
            if treeD_data['objects'][0]['name'] == '영역오류':
                treed = treeD_data['objects'][0]['points']

                x1 = treed[0][0]
                y1 = treed[0][1]
                x2 = treed[1][0]
                y2 = treed[1][1]
                treed = [x1,y1,x2,y2]
                    

            # for treeD in treeD_list:
            #     iou_list = []
            #     cla = None
            #     for label in label_list:

                iou = IoU(bbox, treed)
                # iou_list.append((iou, label))

                # max_iou = max([ i[0] for i in iou_list])
                # cla = [i[1] for i in iou_list if i[0] == max_iou]

                list2df.append([filename, iou])
        
    df = pd.DataFrame(list2df, columns=['파일명', 'IoU값'])
    df.to_excel(f"{output_dir}/IoU.xlsx", index=False)