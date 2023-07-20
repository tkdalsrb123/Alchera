import os
import cv2, json
import xmltodict
from collections import defaultdict
import numpy as np

def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img


input_path = r"C:\Users\Alchera115\wj.alchera\Alchera_data\07\0720_xml_to_json\save"
xml_path = r"C:\Users\Alchera115\wj.alchera\Alchera_data\07\0720_xml_to_json\HLKlemove_poc\HLKlemove_poc\00_xml\poc_annotations.xml"
img_dir = r"C:\Users\Alchera115\wj.alchera\Alchera_data\07\0720_xml_to_json\SD_sample_DB"
output_dir = r"C:\Users\Alchera115\wj.alchera\Alchera_data\07\0720_xml_to_json\img_save"

matching_color = defaultdict()
with open(xml_path, encoding='utf-8') as f:
    xmlstring = f.read()
dict_data = xmltodict.parse(xmlstring)

for label in dict_data['annotations']['meta']['task']['labels']['label']:
    Class = label['name']
    color = label['color']
    matching_color[Class] = color

for key, hex in matching_color.items():
    matching_color[key] = hex_to_rgb(hex[1:])


for root, dirs, files in os.walk(input_path):
    for file in files:
        json_path = os.path.join(root, file)
        
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
            
        imgname = json_file['imagePath']
        img_path = os.path.join(img_dir, imgname)
        
        img = read_img(img_path)
        for shape in json_file['shapes']:
            label = shape['label']
            point = shape['points']
            color = matching_color[label]
            point = np.array([[int(p[0]), int(p[1])] for p in point])
            cv2.fillPoly(img, pts=np.int32([point]), color=color)
        
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        save_path = os.path.join(output_dir, imgname)
        result, encoded_img = cv2.imencode('.jpg', img)
        if result:
            with open(save_path, mode='w+b') as f:
                encoded_img.tofile(f)

            