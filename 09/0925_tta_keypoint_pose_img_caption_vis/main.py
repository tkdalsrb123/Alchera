import json, cv2, os, sys
import logging
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from PIL import Image, ImageFont, ImageDraw

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
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img):
    result, encoded_img = cv2.imencode('.jpg', img)
    logger.info(f"{img_path} 저장!!")
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def vis_text(img, p_text, k_text, e_text):
    
    text = f"포즈:{p_text}\n한글:{k_text}\n영어:{e_text}"
    
    fontpath = "malgunbd.ttf"
    fontSize = 20
    font = ImageFont.truetype(fontpath, fontSize)
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)

    draw.text((0,0), text, (0,0,0), font=font)
    
    result = np.array(img)

    return result

def vis_points(joint_coor):
    joint_list = []
    idx = 0
    for i in range(0, len(joint_coor), 2):
        joint_list.append([round(joint_coor[i]), round(joint_coor[i+1])])
        xy = (round(joint_coor[i]), round(joint_coor[i+1]))
        cv2.circle(img, (xy), 3, color=(0,0,255), thickness=-1)
        # cv2.putText(img, str(idx),(xy), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.3, color=(0,255,0))
        idx += 1
    return joint_list

def vis_line(joint_coor):
    for line in joint_coor:
        pts = [[i[0], i[1]] for i in line]
        pts = np.array(pts)
        cv2.polylines(img, np.int32([pts]), False, (255,0,0))
    # for i in joint_coor:
        # if len(i)>1:
        #     for j in range(len(i)-1):
        #         print(tuple(i[j]), tuple(i[j+1]))
        #         cv2.line(img, tuple(i[j]), tuple(i[j+1]), color=(255,0,0))

        
_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(input_dir, '.jpg')
json_dict = readfiles(input_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    filename = f"{filename}_label"
    json_path = json_dict.get(filename)

    if json_path:
        output_img_path = makeOutputPath(img_path, input_dir, output_dir)
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)

        img =read_img(img_path)
        pos = json_file['normal_info']['포즈']
        kor_caption = json_file['이미지_캡션']['한글']
        eng_caption = json_file['이미지_캡션']['영어']
        
        img = vis_text(img, pos, kor_caption, eng_caption)
        
        joint_pose = json_file['annotations']['joint_pose']
        joint_face = json_file['annotations']['joint_face']
        joint_hand_left = json_file['annotations']['joint_hand_left']
        joint_hand_right = json_file['annotations']['joint_hand_right']
                
        pose_coor = vis_points(joint_pose)
        face_coor = vis_points(joint_face)
        left_coor = vis_points(joint_hand_left)
        right_coor = vis_points(joint_hand_right)

        # pose_line = [[pose_coor[0], pose_coor[15]],
        #              [pose_coor[0], pose_coor[16]],
        #              [pose_coor[1], pose_coor[0]],
        #              [pose_coor[1], pose_coor[2]],
        #              [pose_coor[1], pose_coor[5]],
        #              [pose_coor[1], pose_coor[8]],
        #              [pose_coor[2], pose_coor[1]],
        #              [pose_coor[2], pose_coor[3]],
        #              [pose_coor[3], pose_coor[2]],
        #              [pose_coor[3], pose_coor[4]],
        #              [pose_coor[4], pose_coor[3]],
        #              [pose_coor[5], pose_coor[1]],
        #              [pose_coor[5], pose_coor[6]],
        #              [pose_coor[6], pose_coor[5]],
        #              [pose_coor[7], pose_coor[6]],
        #              [pose_coor[8], pose_coor[1]],
        #              [pose_coor[8], pose_coor[9]],
        #              [pose_coor[8], pose_coor[12]],
        #              [pose_coor[9], pose_coor[8]],
        #              [pose_coor[9], pose_coor[10]],
        #              ]
        # pose_line = [[pose_coor[17], pose_coor[15], pose_coor[0], pose_coor[16], pose_coor[18]],
        #              [pose_coor[0], pose_coor[1], pose_coor[8]],
        #              [pose_coor[2], pose_coor[1], pose_coor[5]],
        #              [pose_coor[2], pose_coor[3], pose_coor[4]],
        #              [pose_coor[5], pose_coor[6], pose_coor[7]],
        #              [pose_coor[9], pose_coor[8], pose_coor[12]],
        #              [pose_coor[9], pose_coor[10], pose_coor[11], pose_coor[22]],
        #              [pose_coor[12], pose_coor[13], pose_coor[14], pose_coor[19]],
        #              [pose_coor[11], pose_coor[24]],
        #              [pose_coor[22], pose_coor[23]],
        #              [pose_coor[14], pose_coor[21]],
        #              [pose_coor[19], pose_coor[20]]]
        # face_line = [[face_coor[0], face_coor[1], face_coor[2], face_coor[3], face_coor[4],face_coor[5],face_coor[6],face_coor[7],face_coor[8],face_coor[9],face_coor[10],face_coor[11],face_coor[12],face_coor[13],face_coor[14],face_coor[15], face_coor[16]],
        #               [face_coor[17], face_coor[18], face_coor[19], face_coor[20], face_coor[21]],
        #               [face_coor[22], face_coor[23], face_coor[24], face_coor[25], face_coor[26]]]

        # vis_line(pose_line)
        # vis_line(face_line)
        save_img(output_img_path, img)

