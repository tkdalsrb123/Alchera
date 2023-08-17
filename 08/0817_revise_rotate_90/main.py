import numpy as np
import xmltodict
import os, sys
from collections import defaultdict
from tqdm import tqdm
from PIL import Image
import shutil

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

def saveXml(pathXml, objXml):
    with open(pathXml, 'w') as f:
        f.write(xmltodict.unparse(objXml, pretty=True))
        
def make_file_dict(input_dir, find_ext):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == find_ext:
                file_path = os.path.join(root, file)
                file_dict[file] = file_path        

    return file_dict

def revise_poly_coor(coordinates, w):
    split_list = coordinates.split(';')
    coor_list = list(map(lambda x: x.split(','), split_list))

    for coor in coor_list:
        x = float(coor[0])
        y = float(coor[1])

        x_new = y
        y_new = w - x

        coor[0] = str(round(x_new, 2))
        coor[1] = str(round(y_new, 2))
    
    return_list = list(map(lambda x: ','.join(x), coor_list))
    new_coordinates = ';'.join(return_list)
    return new_coordinates
    
no_file_list = ['1690341887349002798_color.jpg',
'1690341887848792381_color.jpg',
'1690341888315707068_color.jpg',
'1690341889250654724_color.jpg',
'1690349981948149707_color.jpg',
'1690349982648339029_color.jpg',
'1690349983815393977_color.jpg',
'1690349984748840539_color.jpg']


_, input_img_dir, input_xml_dir, output_img_dir, output_xml_dir = sys.argv

img_dict = make_file_dict(input_img_dir, '.jpg')

xml_list = []
for root, dirs, files in os.walk(input_xml_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.xml':
            xml_path = os.path.join(root, file)
            xml_list.append(xml_path)

rotate_img_list = []
img_list = []
for xml_path in tqdm(xml_list):
    root, file = os.path.split(xml_path)
    mid = '\\'.join(root.split('\\')[len(input_xml_dir):])
    folder = os.path.join(output_xml_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_xml_path = os.path.join(folder, file)
    xml2dict = readxml(xml_path)
    ann = xml2dict['annotations']
    for image in ann['image']:
        img_name = image['@name']
        img_width = int(image['@width'])
        img_height = int(image['@height'])
        if img_width < img_height:
            img_list.append(img_name)
        elif img_width > img_height:
            rotate_img_list.append(img_name)
            image['@width'] = img_height
            image['@height'] = img_width
            
            polygon = image.get('polygon')
            box = image.get('box')

            if polygon is not None:
                if type(polygon) == list:
                    for poly in polygon:
                        points = poly['@points']
                        new_coor = revise_poly_coor(points, img_width)

                        poly['@points'] = new_coor
                        
                elif type(polygon) == dict:
                    points = polygon['@points']
                    new_coor = revise_poly_coor(points, img_width)
                    polygon['@points'] = new_coor
                
            if box is not None:
                if type(box) == dict:
                    x1 = float(box['@xtl'])
                    y1 = float(box['@ytl'])
                    x2 = float(box['@xbr'])
                    y2 = float(box['@ybr'])

                    x1_new = y1
                    y1_new = img_width - x1
                    x2_new = y2
                    y2_new = img_width - x2

                    box['@xtl'] = x1_new
                    box['@ytl'] = y1_new
                    box['@xbr'] = x2_new
                    box['@ybr'] = y2_new
                    
                elif type(box) == list:
                    for b in box:
                        x1 = float(b['@xtl'])
                        y1 = float(b['@ytl'])
                        x2 = float(b['@xbr'])
                        y2 = float(b['@ybr'])
                        
                        x1_new = y1
                        y1_new = img_width - x1
                        x2_new = y2
                        y2_new = img_width - x2
                        
                        b['@xtl'] = x1_new
                        b['@ytl'] = y1_new
                        b['@xbr'] = x2_new
                        b['@ybr'] = y2_new
                        
    saveXml(output_xml_path, xml2dict)
    print(output_xml_path, 'xml 저장!!')

[rotate_img_list.remove(v) for v in rotate_img_list if v in no_file_list]
[img_list.append(v) for v in no_file_list]

for img_name in tqdm(rotate_img_list):
    img_path = img_dict[img_name]
    
    mid = '//'.join(img_path.split('//')[len(input_img_dir):-1])
    folder = os.path.join(output_img_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    output_img_path = os.path.join(folder, img_name)
    img = Image.open(img_path)
    img = img.transpose(Image.ROTATE_90)
    img.save(output_img_path)
    print(output_img_path, 'image 저장!!')
    
for img_name in tqdm(img_list):
    img_path = img_dict[img_name]
    
    mid = '//'.join(img_path.split('//')[len(input_img_dir):-1])
    folder = os.path.join(output_img_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    output_img_path = os.path.join(folder, img_name)
    shutil.copy2(img_path, output_img_path)
    print(output_img_path, 'image 저장!!')