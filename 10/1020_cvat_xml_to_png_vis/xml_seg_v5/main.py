import sys, os
import json
from iter_files import iter_files
from file_io import file_io
from ref_dict import ref_dict
from visual import visual
from text import text
from VISUAL_PREF import VISUAL_PREF
from TEXT_PREF import TEXT_PREF
from tqdm import tqdm
import numpy as np
from collections import deque

def visualize(img_cv2, polygon_list, COLOR_DICT):
    if type(polygon_list) == dict:
        polygon_list = [polygon_list]
    polygon_list.sort(key=lambda p: int(p['@z_order']))

    poly_list = deque([])
    for polygon in polygon_list:
        label = polygon['@label']
        sub_class = ''
        if polygon.get('attribute'):
            if type(polygon['attribute']) is dict:
                sub_class = polygon['attribute']['#text']
            else:
                for att in polygon['attribute']:
                    if att['@name'] == 'Subclass':
                        sub_class = att['#text']

            points_s = polygon['@points']
            points_s_l = points_s.split(';')
            point_s_l = [ p.split(',') for p in points_s_l ]
            point_l = [ [float(p[0]), float(p[1])] for p in point_s_l]
            
            if sub_class == 'Driving lane' or sub_class == 'Counter lane':
                poly_list.appendleft((label, sub_class, point_l))
            else:
                poly_list.append((label, sub_class, point_l))
    for poly in poly_list:
        label, sub_class, point_l = poly
        if (label+sub_class) in VISUAL_PREF.SEGMENT_COLOR_DICT.keys():
            
            BGR = VISUAL_PREF.SEGMENT_COLOR_DICT[label+sub_class]
        else:
            h = COLOR_DICT[label].lstrip('#')
            RGB = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            BGR = (RGB[2], RGB[1], RGB[0])

        img_cv2 = visual.seg(img_cv2, point_l, VISUAL_PREF.SEGMENT_THICKNESS, BGR, alpha=0.0)
        img_cv2 = visual.seg(img_cv2, point_l, VISUAL_PREF.SEGMENT_THICKNESS, (255, 255, 255))
    else:
        pass
    
    return img_cv2 

if __name__ == '__main__':
    
    _, xml_dir, output_dir = sys.argv

    # img_dir_dict = iter_files.iter_files(img_dir, ['.png', '.jpg'])
    xml_list = []
    for root, _, files in os.walk(xml_dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.xml':
                file_path = os.path.join(root, file)
                xml_list.append(file_path)
    
    for xml_path in tqdm(xml_list, desc='read xml', position=0):
    
        xml_data_dict = file_io.open_file(xml_path)

        COLOR_DICT = {'Road': '#D3D3D3', 'HeavyEquipment': '#B22222', 'Cyclist': '#32CD32', 'Motorcycle': '#eb16c0', 'Personal Mobility': '#FFB6C1', 'Misc': '#808000', 'Bus': '#4169E1', 'Truck': '#191970', 'Car': '#8A2BE2', 'Emergency': '#ea0f58', 'Background': '#E6E6FA', 'Motorcycle': '#228B22'}
        # labels = ref_dict.ref_dict(xml_data_dict, ['annotations', 'meta', 'job', 'labels', 'label'])

        # if type(labels) is dict:
        #     labels = [ labels ]

        # for label in labels:
        #     COLOR_DICT[label['name']] = label['color']
        # print(COLOR_DICT)
        IMAGE_DICT = {}
        images = ref_dict.ref_dict(xml_data_dict, ['annotations', 'image'])
        
        if type(images) is dict:
            images = [ images ]

        for image in images:
            basename, _ = os.path.splitext(image['@name'])
            if image.get('polygon'):
                IMAGE_DICT[basename] = [(image['@width'], image['@height']), image['polygon']]
            else:
                IMAGE_DICT[basename] = [(image['@width'], image['@height']), None]

        # for basename in tqdm(img_dir_dict.keys()):

        #     img_path = img_dir_dict[basename]
        #     img_cv2 = file_io.open_file(img_path)
        for basename, img_info in tqdm(IMAGE_DICT.items(), desc='create image', position=1): 
            w, h = img_info[0]
            canvas = np.zeros((int(h), int(w), 3), np.uint8)
            canvas[:] = (250, 230, 230)

            relpath = os.path.relpath(xml_path, xml_dir)
            dir = os.path.split(relpath)[0]
            folder = os.path.join(output_dir, dir)
            os.makedirs(folder, exist_ok=True)
            save_path = os.path.join(folder, f"{basename}.png")

            if IMAGE_DICT[basename][1] != None:
                save_path = save_path.replace("CMR_GT_BB", "CMR_SD_Color")
                result_cv2 = visualize(canvas, IMAGE_DICT[basename][1], COLOR_DICT)
                file_io.save_file(result_cv2, save_path)
            else:
                save_path = save_path.replace("CMR_GT_BB", "CMR_SD_Color")
                print(save_path)
                file_io.save_file(canvas, save_path)
