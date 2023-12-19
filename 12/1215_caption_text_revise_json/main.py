import os, sys, logging, json
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

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def saveJson(file, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)
        
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

def get_true_value(values):
    val = ""
    for value in values:
        if value['selected'] == True:
            val = value['value']
    return val

def bbox_format(_id, _type, points, tabulization_count):
    bbox = {
        "id": _id,
        "type": _type,
        "points": points,
        "tabulization_count": tabulization_count
        }
        
    return bbox

def json_format(outline, total_count, bbox, output_path):
    tree  ={
    "objects": {
        "detail": [
            {
            "outline": outline,
            "total_count": total_count
            }
        ],
        "bbox": bbox
        }
    }
    
    saveJson(tree, output_path)

def contents_format(att_dict, path):
    legend = []
    x_val = []
    y_val = []
    unit = []
    x_name = []
    y_name = []
    integrated = ""
    for k, v in att_dict.items():
        if '범례' in k:
            legend.append(v)
        elif 'X값' in k:
            x_val.append(v)
        elif 'Y값' in k:
            y_val.append(v)
        elif '단위' in k:
            unit.append(v)
        elif 'X축 제목' in k:
            x_name.append(v)
        elif 'Y축 제목' in k:
            y_name.append(v)
        elif '통합성' in k:
            integrated = int(v[0])
    
    error_check(x_val, path)
    error_check(y_val, path)
    error_check(x_val, path)

    contents = []
    for i in range(len(legend)):
        if x_val[i] != "" and y_val[i] !="":
            contents.append({'legend':split_text(legend[i]),
            'x':split_text(x_val[i]),
            'y':split_text(y_val[i]),
            'integrated':integrated,
            'x-unit':split_text(x_name[i]),
            'y-unit':split_text(y_name[i])
            })
        
    return contents

def error_check(val, path):
    if len(val) == 0:
        error_list.append(path)
        
def split_text(value):
    value = value.split('\n')
    if len(value) > 1:
        result = [[v.strip() for v in val.split('#')] for val in value]
    else:
        if value[0]:
            result = [v.strip() for v in value[0].split('#')]
        else:
            result = ['']
    return result
    
def caption_json_format(_type, att_dict, output_file_path, imagename):
    if _type == 'A' or _type == 'B':
        contents = contents_format(att_dict, output_file_path)
        tree = {'title': att_dict['제목'],
                'subtitle': [i for i in [att_dict['부제목_1'], att_dict['부제목_2']] if i != ""],
                'source': [split_text(i) for i in [att_dict['출처_1'], att_dict['출처_2']] if i != ""],
                'additional': [split_text(i) for i in [att_dict['부가설명_1'], att_dict['부가설명_2']] if i != ""],
                'writer': [i for i in [att_dict['작성자_1'], att_dict['작성자_2']] if i != ""],
                'contents':contents,
                'info':[{'origin_imageName':imagename},{'type': _type}]
                }
                
    elif _type == 'C':
        error_check(att_dict['개요(outline)'], output_file_path)
        tree = {'objects': 
                    {'caption':[{'title':'제목', 'text':att_dict['제목(title)']},{'outline':'개요','text':split_text(att_dict['개요(outline)'])}]}, 
                    'info':[{'origin_imageName':imagename}, {'type': _type}]
                }
        
    elif _type == 'D':
        error_check(att_dict['개요(outline)'], output_file_path)
        tree = {
        "ojects": {
            "caption": [
            {
                "title": "제목",
                "text": att_dict['제목(title)']
            },
            {
                "outline": "개요",
                "text": split_text(att_dict['개요(outline)'])
            },
            {
                "additional": "세부내용(외부항목-부가설명)",
                "text": split_text(att_dict['부가설명(additional)'])
            },
            {
                "contents-tabulization": "세부내용(내부항목-그래프수치설명)",
                "text": split_text(att_dict['세부내용(contents-tabulization)'])
            },
            {
                "contents-tendency": "세부내용(경향성)",
                "text": split_text(att_dict['경향성(contents-tendency)'])
            },
            {
                "summary": "요약",
                "text": split_text(att_dict['요약(summary)'])
            },
            {
                "dataaccuracy": "정확도",
                "level": int(att_dict['정확도(dataaccuracy)'][0])
            }
            ]
        },
        "info": [
            {
            "origin_imageName": imagename
            },
            {
            "type": _type
            }
        ]
    }
    saveJson(tree, output_file_path)
    
def make_output_folder(mid, last=None):
    if last:
        folder = os.path.join(output_dir, mid, last)
    else:
        folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)

def make_points(points):
    point = (points[0][0], points[0][1], points[1][0], points[1][1])
    return point

def make_xlsx(_list, col, output_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_excel(output_path, index=False)
    
if __name__ == '__main__':
    _, input_bbox_json_dir, input_caption_json_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    bbox_json_dict = readfiles(input_bbox_json_dir, '.json')
    caption_json_dict = readfiles(input_caption_json_dir, '.json')

    make_output_folder('bbox_json')
    make_output_folder('caption_json','A')
    make_output_folder('caption_json','B')
    make_output_folder('caption_json','C')
    make_output_folder('caption_json','D')

    error_list = []
    result_list = []
    for filename, bbox_json_path in tqdm(bbox_json_dict.items()):
        caption_json_path = caption_json_dict.get(filename)
        if caption_json_path:
            logger.info(caption_json_path)
            # output_json_path = makeOutputPath(json_path, input_dir, output_dir, 'json')
            
            bbox_data = readJson(bbox_json_path)
            caption_data = readJson(caption_json_path)
            
            bbox_info_dict = {}
            bbox_filname = bbox_data['info']['imageName']
            for obj in bbox_data['objects']:
                bbox_info_dict[obj['id']] = (obj['name'], obj['points'])
            
            caption_info_dict = defaultdict(dict)
            for obj in caption_data['objects']:
                if obj['name'] == "이미지 설명":
                    for att in obj['attributes']:
                        caption_info_dict.update({att['name']:get_true_value(att['values'])})
                    
                else:
                    caption_info_dict[obj['id']]['points'] = obj['points']
                    caption_info_dict[obj['id']]['type'] = obj['name']
                    for att in obj['attributes']:
                        caption_info_dict[obj['id']].update({att['name']:get_true_value(att['values'])})
             
  
            bbox_list = []
            for _id, bbox_info in bbox_info_dict.items():
                bbox_type, _bbox_points = bbox_info
                bbox_points = make_points(_bbox_points)
                bbox_filename = os.path.splitext(bbox_filname)[0]
                result_list.append([bbox_filname, f"{bbox_filename}.json", f"{_id}.json", bbox_type])
                tf = True
                for caption_value in caption_info_dict.copy().values():
                    
                    if caption_value and type(caption_value) == dict:
                        bbox_filename = os.path.splitext(bbox_filname)[0]
                        
                        if caption_value['type'] != 'Table' and caption_value['type'] != 'E':
                            caption_points = make_points(caption_value['points'])
                            iou = IoU(bbox_points, caption_points)
                            if iou > 0.5:
                                caption_json_format(caption_value['type'], caption_value, f"{output_dir}/caption_json/{caption_value['type']}/{_id}.json", bbox_filname)
                                bbox_list.append(bbox_format(_id, bbox_type, _bbox_points, caption_value['캡션 가능한 그래프 수(BBox 내)']))
                                tf = False
                        else:
                            bbox_list.append(bbox_format(_id, bbox_type, _bbox_points, '0'))
                            tf = False
                if tf:
                    bbox_list.append(bbox_format(_id, bbox_type, _bbox_points, '0'))
                        
                
                
                
                json_format(caption_info_dict['개요(outline)'], caption_info_dict['캡션 가능한 그래프 개수(전체 이미지 내)'], bbox_list, f"{output_dir}/bbox_json/{bbox_filename}.json")

    make_xlsx(error_list, ['error_list'], f"./error_list.xlsx")
    make_xlsx(result_list, ['img', 'bbox_json', 'tabulization_json', 'type'], f"./result.xlsx")
    
                    