import os, sys, xmltodict, logging
import pandas as pd
from  tqdm import tqdm
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
                sequence = os.path.split(root)[-1]
                file_path = os.path.join(root, file)
            
                file_dict[sequence] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, seq, name, Ext):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, seq, f"{name}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

def saveXml(pathXml, objXml):
    with open(pathXml, 'w', encoding='utf-8') as f:
        f.write(xmltodict.unparse(objXml, pretty=True))

def preprocessing(x):

    if type(x['연령']) == str:
        age = 50
    else:
        age = x['연령']
        
    if x['성별'] == '남':
        gender = 'male'
    else:
        gender = 'female'
        
    if type(x['CVAT ID']) == int:
        info_dict[x['TASK']][x['CVAT ID']] = {'ID':x['ID'], 'gender':gender, 'age':age}

def revise_info(name, val):
    att_list.append({'@name':name, '#text':str(val)})

def xml_format(task, images, output_path):
    format = {"annotations":{"task":task, "image":images}}

    saveXml(output_path, format)
    
def make_xlsx(_list, col, output_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_excel(output_path, index=False)
    
if __name__ == '__main__':
    _, excel_dir, input_dir, output_dir = sys.argv

    info_dict = defaultdict(lambda : defaultdict(dict))
    df = pd.read_excel(excel_dir)
    df.apply(preprocessing, axis=1)

    xml_dict = readfiles(input_dir, '.xml')
    error_list = []
    for sequence, xml_path in tqdm(xml_dict.items(), desc="xml", position=0):
        
        data = readxml(xml_path)
        task_list = data['annotations']['meta']['project']['tasks']['task']

        to_xml_task = {}
        for task in task_list:
            
            if '-' not in task['name']:
                name = task['name']
                _id = task["id"]
                to_xml_task[_id] = {"task":task, "task_name":name}

        image_dict = defaultdict(list)
                
        for i, image in enumerate(tqdm(data['annotations']['image'], desc="gather xml image data", position=1)):
            task_id = image['@task_id']
            task_info = to_xml_task.get(task_id)
            if task_info:
                if len(task_info["task_name"].split('_')) < 5:
                    task_name = task_info["task_name"]
                    info = info_dict.get(task_name)
                else:
                    task_name = '_'.join(task_info["task_name"].split('_')[:-1])
                    info = info_dict.get(task_name)
                    
                if info:

                    box = image.get('box')
                    if box:
                        
                        if type(box) == dict:
                            box = [box]
                        for j, box in enumerate(box):
                            att_list = []
                            if type(box['attribute']) == dict:
                                box_attribute = [box['attribute']]
                            else:
                                box_attribute = box['attribute']
                            
                            for k, attribute in enumerate(box_attribute):
                                
                                if attribute['@name'] == 'id':

                                    id_gender_age = info.get(int(attribute['#text']))
                                    try:
                                        revise_info('id', id_gender_age['ID'])
                                        revise_info('gender', id_gender_age['gender'])
                                        revise_info('age', id_gender_age['age'])
                                    except TypeError:
                                        error_list.append([task_id, task_info['task_name'], box])
                                elif attribute['@name'] == 'id_2':
                                    pass
                                else:
                                    att_list.append(attribute)
                            att_list.append({'@name':'cloth id', '#text':str(task_name.split('_')[-1])})
                            
                            try:
                                data['annotations']['image'][i]['box'][j]['attribute'] = att_list
                            except KeyError:
                                data['annotations']['image'][i]['box']['attribute'] = att_list
                                
                        
                        image_dict[task_id].append(data['annotations']['image'][i])

        make_xlsx(error_list, ['id', 'sequence', 'box'], "./error_list.xlsx")
        
        for task_id, image_data in tqdm(image_dict.items(), desc="create xml"):
            task = to_xml_task[task_id]['task']
            task_name = to_xml_task[task_id]['task_name']
            output_xml_path = makeOutputPath(xml_path, input_dir, output_dir, sequence, task_name, 'xml')
            xml_format(task, image_data, output_xml_path)
            