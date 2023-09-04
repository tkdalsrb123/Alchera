import cv2, json, sys, os
from collections import defaultdict
import numpy as np
import logging
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

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def readfiles(dir, Ext):
    file_dict = defaultdict(list)
    if Ext == 'json':
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.json':
                    filename = '_'.join(filename.split('_')[:5])
                    
                    file_path = os.path.join(root, file)
                    
                    file_dict[filename].append(file_path)
                    
        return file_dict

    elif Ext == 'img':
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.jpg' or ext == '.png':
                    file_path = os.path.join(root, file)

                    file_dict[filename] = file_path
        return file_dict
    

_, img_dir, json_dir, output_dir, point_dir = sys.argv

logger = make_logger('log.log')

key_point_dict = {'nose':'0', 'the left eye':'1', 'the right eye':'2' , 'the left ear':'3', 'the right ear':'4', 'the left shoulder':'5', 'the right shoulder':'6', 'the left elbow':'7', 'the right elbow':'8',
             'the left wrist':'9', 'the right wrist':'10', 'the left hip':"11", 'the right hip':'12', 'the left knee':'13', 'the right knee':'14', 'the left ankle':'15',
             'the right ankle':'16'}

json_dict = readfiles(json_dir, "json")
img_dict = readfiles(img_dir, 'img')
point_dict = readfiles(point_dir, 'json')

point_info = defaultdict(str)

for point_path in point_dict.values():
    with open(point_path[0], encoding='utf-8') as f:
        point_file = json.load(f)
    for obj in point_file['objects']:
        point_info[obj['file_name']] = [obj['points'], obj['bbox']]

for filename, img_path in tqdm(img_dict.items()):
    json_path_list = json_dict[filename]
    
    root, file = os.path.split(img_path)
    mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_img_path = os.path.join(folder, file)

    img = read_img(img_path)

    for json_path in json_path_list:
        logger.info(json_path)
            
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        
        point_dict = defaultdict(str)
        keypoints = []
        for obj in json_file['objects']:
            name = obj['name']
            have_keypoint = key_point_dict.get(name)
            
            if have_keypoint != None:
                
                keypoints.append(obj['points'])
  
        na = os.path.split(json_path)[-1]
        bb_x1 = point_info[na][1][0]
        bb_y1 = point_info[na][1][1]
        
        # x, y, w, h = cv2.boundingRect(np.array(keypoints, dtype=np.float32))

        # diff_x = abs(bb_x1 - (x))
        # diff_y = abs(bb_y1 - (y))
        
        for obj in json_file['objects']:
            name = obj['name']
            have_keypoint = key_point_dict.get(name)
            
            if have_keypoint != None:
                points = obj['points']
                point_text = key_point_dict[name]          
                for val in obj['attributes'][0]['values']:
                    if val['selected'] == True:
                        if val['value'] == 'truncation':
                            color = (255, 0, 0)
                        elif val['value'] == 'visible':
                            color = (0, 255, 255)
                        elif val['value'] == 'invisible':
                            color = (0, 255, 0)

                points[0][0] += bb_x1 - 20
                points[0][1] += bb_y1 

                cv2.circle(img, (round(points[0][0]),round(points[0][1])), 3, color=color, thickness=-1)
                cv2.putText(img, point_text,(round(points[0][0])-5,round(points[0][1])-2), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.3, color=color)
                    
                point_dict[point_text] = points
                

        head = [point_dict['4'], point_dict['2'], point_dict['0'], point_dict['1'], point_dict['3']]
        right_arm = [point_dict['6'], point_dict['8'], point_dict['10']]
        left_arm = [point_dict['5'], point_dict['7'], point_dict['9']]
        body = [point_dict['5'], point_dict['6'], point_dict['12'], point_dict['11'], point_dict['5']]
        right_leg = [point_dict['12'], point_dict['14'], point_dict['16']]
        left_leg = [point_dict['11'], point_dict['13'], point_dict['15']]
        
        line_vis_list = [head, right_arm, left_arm, body, right_leg, left_leg]

        for line in line_vis_list:
            pts = [[round(i[0][0]), round(i[0][1])] for i in line]
            pts = np.array(pts)
            cv2.polylines(img, np.int32([pts]), False, (0, 69, 255))


    result, encoded_img = cv2.imencode('.jpg', img)
    if result:
        with open(output_img_path, mode='w+b') as f:
            encoded_img.tofile(f)