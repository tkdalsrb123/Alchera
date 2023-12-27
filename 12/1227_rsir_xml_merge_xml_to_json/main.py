import os, sys, json, xmltodict, logging
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
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    return data 

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

def saveXml(pathXml, objXml):
    with open(pathXml, 'w') as f:
        f.write(xmltodict.unparse(objXml, pretty=True))

def polygon_format(data, _case=None):
    if data:
        if _case:
            if len(data['points'])>0:
                points = data['points'][0]
                format = {'@label': 'Road', '@occluded': '0', '@source': 'manual', '@points': points, '@z_order': '-1', 'attribute': {'@name': 'subClass', '#text': _case}}
                polygon_list.append(format)
        else:
            for obj in data:
                format = {'@label': obj['class'] , '@occluded': '0', '@source': 'manual', '@points': obj['segmentation']['points'][0], '@z_order': '0', 'attribute': [{'@name': 'subClass', '#text': obj['sub_class']}, {'@name': 'ID', '#text': obj['id']}]}
                polygon_list.append(format)

if __name__ == "__main__":
    _, xml_dir, json_dir, output_dir = sys.argv
    
    xml_dict = readfiles(xml_dir, '.xml')
    json_dict = readfiles(json_dir, '.json')

    for filename, xml_path in tqdm(xml_dict.items(), desc="read xml", position=0):
        output_xml_path = makeOutputPath(xml_path, xml_dir, output_dir, 'xml')
        data = readxml(xml_path)

        for image in tqdm(data['annotations']['image'], desc='revise xml', position=1):

            filename = os.path.splitext(image['@name'])[0]
            json_path = json_dict.get(filename)
            if json_path:

                json_data = readJson(json_path)
                
                polygon_list = []

                drivinglane = json_data['backgrounds'].get('drivinglane')
                counterlane = json_data['backgrounds'].get('counterlane')
                backgrounds = json_data['backgrounds'].get('backgrounds')
                object = json_data.get('object')
                polygon_format(drivinglane, 'Driving lane')
                polygon_format(counterlane, 'Counter lane')
                polygon_format(backgrounds, 'Background')
                polygon_format(object)
                
                image['polygon'] = polygon_list

        saveXml(output_xml_path, data)
            

            
            
    
    