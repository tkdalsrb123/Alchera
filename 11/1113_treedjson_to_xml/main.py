import os, sys, json
import xmltodict
import logging
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

def saveXml(pathXml, objXml):
    with open(pathXml, 'w') as f:
        f.write(xmltodict.unparse(objXml, pretty=True))

def make_object(name, xmin, ymin, xmax, ymax):
    objects = {"name": name, "pose": "Unspecified", "truncated": "0", "difficult": "0", 
                "bndbox": {"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax}}
    return objects

def xmlformat(output_xml_path, folder, filename, width, height, objects):
    xml = {"annotation": {
        "folder": folder,
        "filename": filename,
        "path": "path",
        "source": {"database": "Unknown"},
        "size": {"width": width, "height": height, "depth": "0"},
        "segmented": "0",
        "object": objects }}
    
    saveXml(output_xml_path, xml)
    logger.info(output_xml_path)
    
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')

    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        output_xml_path = makeOutputPath(json_path, input_dir, output_dir, 'xml')

        data = readJson(json_path)

        objects = []
        for obj in data['objects']:
            xml_obj = make_object(obj['name'], obj['points'][0][0], obj['points'][0][1], obj['points'][1][0], obj['points'][1][1])
            objects.append(xml_obj)
        
        folder = filename.split('_')[0] 
        imagename = f"{filename}.jpg"
        width = data['info']['width']
        height = data['info']['height']
        
        xmlformat(output_xml_path, folder, filename, width, height, objects)