import os, sys, json, logging
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

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

def saveJson(file, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)

def json_format(_type, att_dict, output_file_path):
    if _type == 'A' or _type == 'B':
        tree = {'title': att_dict['제목'],
                'subtitle': att_dict['부제목'],
                'source': att_dict['출처'],
                'additional': att_dict['부가설명'],
                'writer': att_dict['작성자'],
                'contents':[{
                    'legend':att_dict['범례'],
                    'x': att_dict['X값'],
                    'y': [att_dict['Y값']],
                    'integrated': att_dict['통합성'],
                    'unit': att_dict['단위'],
                    'x-unit': att_dict['X축 제목'],
                    'y_unit': att_dict['Y축 제목']}],
                'info':[{'origin_imageName':att_dict['imageName']},{'type': _type}]
                }
                
    elif _type == 'C':
        tree = {'objects': 
                    {'caption':[{'title':'제목', 'text':att_dict['제목(title)']},{'outline':'개요','text':att_dict['개요(outline)']}]}, 
                    'info':[{'origin_imageName':att_dict['imageName']}, {'type': _type}]
                }
        
    elif _type == 'D':
        tree = {
        "ojects": {
            "caption": [
            {
                "title": "제목",
                "text": att_dict['제목(title)']
            },
            {
                "outline": "개요",
                "text": att_dict['개요(outline)']
            },
            {
                "additional": "세부내용(외부항목-부가설명)",
                "text": att_dict['부가설명(additional)']
            },
            {
                "contents-tabulization": "세부내용(내부항목-그래프수치설명)",
                "text": att_dict['세부내용(contents-tabulization)']
            },
            {
                "contents-tendency": "세부내용(경향성)",
                "text": att_dict['경향성(contents-tendency)']
            },
            {
                "summary": "요약",
                "text": att_dict['요약(summary)']
            },
            {
                "dataaccuracy": "정확도",
                "level": att_dict['정확도(dataaccuracy)']
            }
            ]
        },
        "info": [
            {
            "origin_imageName": att_dict['imageName']
            },
            {
            "type": _type
            }
        ]
    }
    saveJson(tree, output_file_path)

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')

    error_list = []
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        data = readJson(json_path)
        
        att_dict = {}
        att_dict['imageName'] = f"{filename}.jpg"
        for objects in data['objects']:
            
            name = objects['name'] # json type
            if name in ['A', 'B']:
                
                json_filename = objects['id'] # json file name
                for attributes in objects['attributes']:
                    if attributes['name'] in ['제목', '부제목', 'X축 제목', 'Y축 제목', '출처', '작성자']:
                        att_dict[attributes['name']] = [attributes['values'][0]['value']]
                    elif attributes['name'] in ['부가설명', '단위', '범례', 'X값', 'Y값']:
                        value = attributes['values'][0]['value']
                        if attributes['name'] in ['X값', 'Y값'] and not value:                            
                            error_list.apped(json_filename, attributes['name'])
                        value = value.split('\n')
                        if len(value) > 1:
                            att_dict[attributes['name']] = [[v.strip() for v in val.split('#')] for val in value]
                        else:
                            if value[0]:
                                att_dict[attributes['name']] = [v.strip() for v in value[0].split('#')]
                            else:
                                att_dict[attributes['name']] = ['']
                    elif attributes['name'] in ['통합성']:
                        for values in attributes['values']:
                            if values['selected'] == True:
                                att_dict[attributes['name']] = [int(values['value'][0])] 
            elif name in ['C', 'D']:
                json_filename = objects['id'] # json file name
                for attributes in objects['attributes']:
                    if attributes['name'] in ['제목(title)', '개요(outline)', '부가설명(additional)', '세부내용(contents-tabulization)', '경향성(contents-tendency)', '요약(summary)']:
                        value = attributes['values'][0]['value']
                        if attributes['name'] in ['개요(outline)'] and not value:                            
                            error_list.apped(json_filename, attributes['name'])
                        att_dict[attributes['name']] = value

                    elif attributes['name'] in ['정확도(dataaccuracy)']:
                        for values in attributes['values']:
                            if values['selected'] == True:
                                att_dict[attributes['name']] = int(values['value'][0])
            
            else:
                continue
            
            output_folder = os.path.join(output_dir, name)
            os.makedirs(output_folder, exist_ok=True)
            output_json_path = os.path.join(output_folder, f"{json_filename}.json")
            json_format(name, att_dict, output_json_path)

            df = pd.DataFrame(error_list, columns=['filename', 'name'])
            df.to_excel(f'{output_dir}/error_list.xlsx', index=False)