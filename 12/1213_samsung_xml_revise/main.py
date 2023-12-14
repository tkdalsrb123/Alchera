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

def makeOutputPath(file_path, file_dir, output_dir, seq, Ext):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{seq}.{Ext}")
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
    
if __name__ == '__main__':
    _, excel_dir, input_dir, output_dir = sys.argv

    info_dict = defaultdict(lambda : defaultdict(dict))
    df = pd.read_excel(excel_dir)
    df.apply(preprocessing, axis=1)

    xml_dict = readfiles(input_dir, '.xml')

    for sequence, xml_path in xml_dict.items():
        task = '_'.join(sequence.split('-')[0].split('_')[1:])
        
        info = info_dict[task]

        output_xml_path = makeOutputPath(xml_path, input_dir, output_dir, sequence, 'xml')
        data = readxml(xml_path)
        for i, image in enumerate(data['annotations']['image']):
            for j, box in enumerate(image['box']):
                att_list = []
                # print(box['attribute'])
                for k, attribute in enumerate(box['attribute']):
                    
                    if attribute['@name'] == 'id':
                        id_gender_age = info.get(int(attribute['#text']))
                        revise_info('id', id_gender_age['ID'])
                        revise_info('gender', id_gender_age['gender'])
                        revise_info('age', id_gender_age['age'])
                    elif attribute['@name'] == 'id_2':
                        pass
                    else:
                        att_list.append(attribute)
                att_list.append({'@name':'cloth id', '#text':str(task.split('_')[-1])})

                data['annotations']['image'][i]['box'][j]['attribute'] = att_list

        saveXml(output_xml_path, data)