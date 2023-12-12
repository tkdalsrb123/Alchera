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
  
def polygon_format(name, points):
    format = {'@label':name, '@occluded':'0', '@source':'manual', '@points':points, '@z_order':'0'}
    return format

def image_format(idx, filename, polygon_list):
    image = {'@id':idx, '@name':filename, '@width':"1920" , '@height':"1080", "polygon":polygon_list}
    return image     
 
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')

    idx = 0
    xml_format = {'annotations': {'version': '1.1', 'meta': {'task': {'id': '5541', 'name': 'test', 'size': '1', 'mode': 'annotation', 'overlap': '0', 'bugtracker': None, 'created': '2023-12-12 02:27:45.820715+00:00', 'updated': '2023-12-12 02:27:46.215630+00:00', 'subset': 'default', 'start_frame': '0', 'stop_frame': '0', 'frame_filter': None, 'segments': {'segment': {'id': '92962', 'start': '0', 'stop': '0', 'url': 'http://ec2-3-39-119-239.ap-northeast-2.compute.amazonaws.com:8080/api/jobs/92962'}}, 'owner': {'username': 'hi.lee', 'email': 'hi.lee@alcherainc.com'}, 'assignee': None, 'labels': {'label': [{'name': 'Soil', 'color': '#faa9e2', 'type': 'any', 'attributes': None}, {'name': 'Background', 'color': '#000000', 'type': 'any', 'attributes': None}, {'name': 'Self', 'color': '#138e0a', 'type': 'any', 'attributes': None}, {'name': 'Obstacle', 'color': '#411413', 'type': 'any', 'attributes': None}, {'name': 'Human', 'color': '#c080e0', 'type': 'any', 'attributes': None}, {'name': 'Dump', 'color': '#715c3b', 'type': 'any', 'attributes': None}]}}, 'dumped': '2023-12-12 02:29:34.272894+00:00'}, 'image': []}}
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        output_xml_path = makeOutputPath(json_path, input_dir, output_dir, 'xml')

        data = readJson(json_path)
        
        file_name = data['Images'][0]['file_name']
        height = data['Images'][0]['height']
        width = data['Images'][0]['width']
        
        
        cat_dict = {}
        for cat in data['Categories']:
            cat_dict[cat['id']] = cat['name']

        polygon_list = []
        for annotation in data['Annotations']:
            name = cat_dict[annotation['segments_info'][0]['category_id']]
            segmentation = annotation['segments_info'][0]['segmentation'][0]
            points_list = [','.join([str(float(segmentation[i])),str(float(segmentation[i+1]))]) for i in range(0, len(segmentation), 2)]
            points = ';'.join(points_list)
            polygon = polygon_format(name, points)
            polygon_list.append(polygon)

        image = image_format(idx, file_name, polygon_list)

        xml_format['annotations']['image'].append(image)
        idx += 1
        
    saveXml(f"{output_dir}/081-102_annotation.xml", xml_format)