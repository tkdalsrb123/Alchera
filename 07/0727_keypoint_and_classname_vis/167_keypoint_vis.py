import os, sys, json
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict
import random

def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def extract_file(path_list, ext):
    for path in path_list:
        if os.path.splitext(path)[-1] == ext:
            return path

        
        
_, input_dir, ouput_dir = sys.argv

# 파일 수집
matching_dict = defaultdict(list)
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            matching_dict[filename].append(json_path)
        
        elif ext == '.png':
            image_path = os.path.join(root, file)
            matching_dict[filename].append(image_path)

for path in matching_dict.values():
    json_path = extract_file(path, '.json')
    image_path = extract_file(path, '.png')
    
    print(image_path, '시각화!!')
    root, file = os.path.split(image_path)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    action_name = json_file['annotationImageInfo']['action']
    
    for obj in json_file['annotationObjectInfo']:
        action_value = obj['actionValue']
        if len(obj['keypoints']) > 0:
            coordinates = obj['keypoints']
        else:
            coordinates = obj['BBox']
        img = Image.open(image_path)
        
        fontsize = 15
        fontpath = 'arial.ttf'
        
        font = ImageFont.truetype(fontpath, fontsize)
        draw = ImageDraw.Draw(img)
        
        random_color = random_color_generator()
        text = f'{action_name}/{action_value}'
        
        if len(coordinates) > 4:
            coordinates = tuple(coordinates)
            draw.line(coordinates, fill=random_color, width=4)
            draw.text((coordinates[0], coordinates[1]+15), action_name, fill=random_color, font=font)
        # else:
            # coordinates = tuple(coordinates)
            # print(coordinates)
            # x1 = coordinates[0]
            # y1 = coordinates[2]
            # x2 = coordinates[1]
            # y2 = coordinates[3]
            # draw.rectangle([(x1,y1), (x2,y2)], fill=random_color, width=4)
            # draw.text((coordinates[0], coordinates[1]+15), action_name, fill=random_color, font=font)
        
        # draw.line(coordinates, fill=random_color, width=4)
        # # for idx in range(0, len(coordinates), 2):
        # #     draw.point((coordinates[idx], coordinates[idx+1]), fill=random_color)
        # draw.text((coordinates[0], coordinates[1]+15), action_name, fill=random_color, font=font)
    
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(ouput_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    save_img_path = os.path.join(folder, file)
    
    img.save(save_img_path, 'png')

    