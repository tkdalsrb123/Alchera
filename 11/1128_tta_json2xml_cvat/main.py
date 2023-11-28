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

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
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

def polygon_format(name, points):
    format = {'@label':name, '@occluded':'0', '@source':'manual', '@points':points, '@z_order':'0'}
    return format

def image_format(idx, filename, polygon_list):
    image = {'@id':idx, '@name':filename, '@width':"1920" , '@height':"1080", "polygon":polygon_list}
    return image

category = {
        3: "Car",
        2: "Two-wheel Vehicle",
        99: "Personal Mobility",
        8: "TruckBus",
        97: "Kid student",
        98: "Adult",
        12: "Traffic Sign",
        10: "Traffic Light",
        52: "Speed bump",
        51: "Parking space",
        100: "Crosswalk",
        3: "car-b",
        2: "Two-wheel Vehicle-b",
        8: "TruckBus-b",
        1: "Pedestrian-b"
    }

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
  
    json_dict = readfiles(input_dir, '.json')

    idx = 0
    xml_format = {'annotations':{'version': '1.1', 'meta': {'task': {'id': '5318', 'name': 'test_xml', 'size': '480', 'mode': 'annotation', 'overlap': '0', 'bugtracker': None, 'created': '2023-11-28 07:11:34.387303+00:00', 'updated': '2023-11-28 07:21:52.680731+00:00', 'subset': 'default', 'start_frame': '0', 'stop_frame': '479', 'frame_filter': None, 'segments': {'segment': {'id': '90996', 'start': '0', 'stop': '479', 'url': 'http://ec2-3-39-119-239.ap-northeast-2.compute.amazonaws.com:8080/api/jobs/90996'}}, 'owner': {'username': 'he.choi', 'email': 'he.choi@alcherainc.com'}, 'assignee': None, 'labels': {'label': [{'name': 'Car', 'color': '#2080c0', 'type': 'polygon', 'attributes': None}, {'name': 'Two-wheel Vehicle', 'color': '#ddff33', 'type': 'any', 'attributes': None}, {'name': 'Personal Mobility', 'color': '#ff007c', 'type': 'any', 'attributes': None}, {'name': 'TruckBus', 'color': '#fa7dbb', 'type': 'any', 'attributes': None}, {'name': 'Kid student', 'color': '#121a12', 'type': 'polygon', 'attributes': None}, {'name': 'Adult', 'color': '#6bdc13', 'type': 'any', 'attributes': None}, {'name': 'Traffic Sign', 'color': '#502080', 'type': 'polygon', 'attributes': None}, {'name': 'Traffic Light', 'color': '#d0a000', 'type': 'polygon', 'attributes': None}, {'name': 'Speed bump', 'color': '#41278a', 'type': 'polygon', 'attributes': None}, {'name': 'Parking space', 'color': '#4de134', 'type': 'polygon', 'attributes': None}, {'name': 'Crosswalk', 'color': '#802040', 'type': 'polygon', 'attributes': None}, {'name': 'Crosswalk', 'color': '#8c3653', 'type': 'polygon', 'attributes': None}]}}, 'dumped': '2023-11-28 07:26:35.419516+00:00'},'image':[]}}
    for filename, json_path in tqdm(json_dict.items()):
        data = readJson(json_path)

        annotations = data['annotations']

        polygon_list = []
        for annotations in data['annotations']:
            name = category[annotations['category_id']]

            points_list = annotations['segmentation']['coord']['points'][0][0]
            points_list = [','.join([str(float(points['x'])),str(float(points['y']))]) for points in points_list]
            points = ';'.join(points_list)
            polygon = polygon_format(name, points)
            polygon_list.append(polygon)
        image = image_format(idx, filename, polygon_list)

        xml_format['annotations']['image'].append(image)
        idx += 1

    saveXml(f"{output_dir}/044-058_annotation.xml", xml_format)
    