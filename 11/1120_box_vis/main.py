import cv2, os, sys, json
import pandas as pd
import numpy as np
import logging
import shutil
import xmltodict
import math
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

class DashedImageDraw(ImageDraw.ImageDraw):

    def thick_line(self, xy, direction, fill=None, width=0):
        #xy – Sequence of 2-tuples like [(x, y), (x, y), ...]
        #direction – Sequence of 2-tuples like [(x, y), (x, y), ...]
        if xy[0] != xy[1]:
            self.line(xy, fill = fill, width = width)
        else:
            x1, y1 = xy[0]            
            dx1, dy1 = direction[0]
            dx2, dy2 = direction[1]
            if dy2 - dy1 < 0:
                x1 -= 1
            if dx2 - dx1 < 0:
                y1 -= 1
            if dy2 - dy1 != 0:
                if dx2 - dx1 != 0:
                    k = - (dx2 - dx1)/(dy2 - dy1)
                    a = 1/math.sqrt(1 + k**2)
                    b = (width*a - 1) /2
                else:
                    k = 0
                    b = (width - 1)/2
                x3 = x1 - math.floor(b)
                y3 = y1 - int(k*b)
                x4 = x1 + math.ceil(b)
                y4 = y1 + int(k*b)
            else:
                x3 = x1
                y3 = y1 - math.floor((width - 1)/2)
                x4 = x1
                y4 = y1 + math.ceil((width - 1)/2)
            self.line([(x3, y3), (x4, y4)], fill = fill, width = 1)
        return   
        
    def dashed_line(self, xy, dash=(2,2), fill=None, width=0):
        #xy – Sequence of 2-tuples like [(x, y), (x, y), ...]
        for i in range(len(xy) - 1):
            x1, y1 = xy[i]
            x2, y2 = xy[i + 1]
            x_length = x2 - x1
            y_length = y2 - y1
            length = math.sqrt(x_length**2 + y_length**2)
            dash_enabled = True
            postion = 0
            try:
                while postion <= length:
                    for dash_step in dash:
                        if postion > length:
                            break
                        if dash_enabled:
                            start = postion/length
                            end = min((postion + dash_step - 1) / length, 1)
                            self.thick_line([(round(x1 + start*x_length),
                                            round(y1 + start*y_length)),
                                            (round(x1 + end*x_length),
                                            round(y1 + end*y_length))],
                                            xy, fill, width)
                        dash_enabled = not dash_enabled
                        postion += dash_step
            except ZeroDivisionError:
                vis_error_list.append([filename, ([x1, y1], [x2, y2])])
        return

    def dashed_rectangle(self, xy, dash=(2,2), outline=None, width=0):
        #xy - Sequence of [(x1, y1), (x2, y2)] where (x1, y1) is top left corner and (x2, y2) is bottom right corner
        x1, y1 = xy[0]
        x2, y2 = xy[1]
        halfwidth1 = math.floor((width - 1)/2)
        halfwidth2 = math.ceil((width - 1)/2)
        min_dash_gap = min(dash[1::2])
        end_change1 = halfwidth1 + min_dash_gap + 1
        end_change2 = halfwidth2 + min_dash_gap + 1
        odd_width_change = (width - 1)%2        
        self.dashed_line([(x1 - halfwidth1, y1), (x2 - end_change1, y1)],
                         dash, outline, width)       
        self.dashed_line([(x2, y1 - halfwidth1), (x2, y2 - end_change1)],
                         dash, outline, width)
        self.dashed_line([(x2 + halfwidth2, y2 + odd_width_change),
                          (x1 + end_change2, y2 + odd_width_change)],
                         dash, outline, width)
        self.dashed_line([(x1 + odd_width_change, y2 + halfwidth2),
                          (x1 + odd_width_change, y1 + end_change2)],
                         dash, outline, width)
        return

def legend():
    font = ImageFont.truetype(fontpath, 15)
    draw.text((0, 0), '■ vehicle', font=font,  fill=(000, 255, 000))
    draw.text((70, 0), '■ emergency', font=font, fill=(255, 000, 000))
    draw.text((180, 0), '■ vehicle whole', font=font, fill=(225, 255, 000))
    draw.text((300, 0), '■ emergency whole', font=font, fill=(50, 200, 150))
    draw.text((460, 0), '■ ptw', font=font, fill=(000, 255, 255))    
    draw.text((520, 0), '■ misc', font=font, fill=(51, 000, 255))
    draw.text((600, 0),  '--- 가림', font=font, fill=(255, 255, 255))
    draw.text((700, 0), '....... 잘림', font=font, fill=(255, 255, 255))
    
def select_outline(Class):
    if Class == 'vehicle':
        return (000, 255, 000)
    elif Class == 'emergency':
        return (255, 000, 000)
    elif Class == 'vehicle whole':
        return (225, 255, 000)
    elif Class == 'emergency whole':
        return (50, 200, 150)
    elif Class == 'ptw':
        return (000, 255, 255)
    elif Class == 'misc':
        return (51, 000, 255)

def select_color(Class):
    if Class == 'vehicle':
        return (255, 000, 255)
    elif Class == 'emergency':
        return (255, 255, 255)
    elif Class == 'vehicle whole':
        return (50, 50, 255)
    elif Class == 'emergency whole':
        return (150, 50, 50)
    elif Class == 'ptw':
        return (255, 255, 255)
    elif Class == 'misc':
        return (255, 255, 255)
    
def visualization(obj):
    for pil in obj:
        if pil['occlusion'] == '0' and pil['truncation'] == '0':
            pil_text = pil['sub_class1'][:3] + '/' + pil['sub_class2'][:3]
            x1 = pil['xmin']
            y1 = pil['ymin']
            x2 = pil['xmin'] + pil['width']
            y2 = pil['ymin'] + pil['height']
            outline = select_outline(pil['class'].lower())
            if pil['sub_class1'][:3] != 'fix':
                draw.rectangle(((x1, y1),(x2, y2)), outline=outline, width=1)
                draw.text((x1, y1-18), pil_text, font=font, fill=outline)
            elif pil['sub_class1'][:3] == 'fix':
                if pil['sub_class2'][:3] == 'lig':
                    pil_text = pil['sub_class2'][:3]
                    draw.rectangle(((x1, y1),(x2, y2)), outline=outline, width=1)
                    draw.text((x2, y1), pil_text, font=font, fill=outline)
                else:
                    pil_text = pil['sub_class2'][:3]
                    draw.rectangle(((x1, y1),(x2, y2)), outline=outline, width=1)
                    draw.text((x1, y1-18), pil_text, font=font, fill=outline)
        elif pil['occlusion'] != '0':
            occlusion = pil['occlusion']
            truncation = pil['truncation']
            text = f'{occlusion} {truncation}'

            ymax = pil['ymax']
            
            pil_text = pil['sub_class1'][:3] + '/' + pil['sub_class2'][:3]
            x1 = pil['xmin']
            y1 = pil['ymin']
            x2 = pil['xmin'] + pil['width']
            y2 = pil['ymin'] + pil['height']
            outline = select_outline(pil['class'].lower())
            if pil['sub_class1'][:3] != 'fix':
                d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(7,5), outline=outline, width=1)
                draw.text((x1, y1-18), pil_text, font=font, fill=outline)
                draw.text((x1, ymax), text, font=sub_font, fill=outline)
            elif pil['sub_class1'][:3] == 'fix':
                if pil['sub_class2'][:3] == 'lig':
                    pil_text = pil['sub_class2'][:3]
                    d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(7,5), outline=outline, width=1)
                    draw.text((x2, y1), pil_text, font=font, fill=outline)
                    draw.text((x1, ymax), text, font=sub_font, fill=outline)
                else:
                    pil_text = pil['sub_class2'][:3]
                    d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(7,5), outline=outline, width=1)
                    draw.text((x1, y1-15), pil_text, font=font, fill=outline)
                    draw.text((x1, ymax), text, font=sub_font, fill=outline)
        elif pil['truncation'] != '0':
            occlusion = pil['occlusion']
            truncation = pil['truncation']
            text = f'{occlusion} {truncation}'

            ymax = pil['ymax']
            
            pil_text = pil['sub_class1'][:3] + '/' + pil['sub_class2'][:3]
            x1 = pil['xmin']
            y1 = pil['ymin']
            x2 = pil['xmin'] + pil['width']
            y2 = pil['ymin'] + pil['height']
            outline = select_outline(pil['class'].lower())
            if pil['sub_class1'][:3] != 'fix':
                d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(1,1), outline=outline, width=1)
                draw.text((x1, y1-15), pil_text, font=font, fill=outline)
                draw.text((x1, ymax+5), text, font=sub_font, fill=outline)
            elif pil['sub_class1'][:3] == 'fix':
                if pil['sub_class2'][:3] == 'lig':
                    pil_text = pil['sub_class2'][:3]
                    d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(1,1), outline=outline, width=1)
                    draw.text((x2, y1), pil_text, font=font, fill=outline)
                    draw.text((x1, ymax+5), text, font=sub_font, fill=outline)
                else:
                    pil_text = pil['sub_class2'][:3]
                    d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(1,1), outline=outline, width=1)
                    draw.text((x1, y1-18), pil_text, font=font, fill=outline)
                    draw.text((x1, ymax+5), text, font=sub_font, fill=outline)

def text_background(obj):
    font = cv2.FONT_HERSHEY_PLAIN
    for pil in obj:
        if pil['occlusion'] == '0' and pil['truncation'] == '0':
            pil_text = pil['sub_class1'][:3] + '/' + pil['sub_class2'][:3]
            (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
            x1 = int(pil['xmin'])
            y1 = int(pil['ymin'])
            x2 = int(pil['xmin'] + pil['width'])
            y2 = int(pil['ymin'] + pil['height'])
            color = select_color(pil['class'].lower())
            if pil['sub_class1'][:3] != 'fix':
                cv2.rectangle(overlay, (x1, y1-text_height-6), (x1+text_width-6, y1), color, -1)
            elif pil['sub_class1'][:3] == 'fix':
                if  pil['sub_class2'][:3] == 'lig':
                    pil_text = pil['sub_class2'][:3]
                    (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
                    cv2.rectangle(overlay, (x2, y1), (x2+text_width, y1+text_height+13), color, -1)
                else:
                    pil_text = pil['sub_class2'][:3]
                    (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
                    cv2.rectangle(overlay, (x1, y1-text_height-6), (x1+text_width, y1), color, -1)
        elif pil['occlusion'] != '0':
            pil_text = pil['sub_class1'][:3] + '/' + pil['sub_class2'][:3]
            (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
            x1 = int(pil['xmin'])
            y1 = int(pil['ymin'])
            x2 = int(pil['xmin'] + pil['width'])
            y2 = int(pil['ymin'] + pil['height'])
            color = select_color(pil['class'].lower())
            if pil['sub_class1'][:3] != 'fix':
                cv2.rectangle(overlay, (x1, y1-text_height-6), (x1+text_width-6, y1), color, -1)
            elif pil['sub_class1'][:3] == 'fix':
                if  pil['sub_class2'][:3] == 'lig':
                    pil_text = pil['sub_class2'][:3]
                    (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
                    cv2.rectangle(overlay, (x2, y1), (x2+text_width, y1+text_height+5), color, -1)
                else:
                    pil_text = pil['sub_class2'][:3]
                    (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
                    cv2.rectangle(overlay, (x1, y1-text_height-6), (x1+text_width, y1), color, -1)
        elif pil['truncation'] != '0':
            pil_text = pil['sub_class1'][:3] + '/' + pil['sub_class2'][:3]
            (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
            x1 = int(pil['xmin'])
            y1 = int(pil['ymin'])
            x2 = int(pil['xmin'] + pil['width'])
            y2 = int(pil['ymin'] + pil['height'])
            color = select_color(pil['class'].lower())
            if pil['sub_class1'][:3] != 'fix':
                cv2.rectangle(overlay, (x1, y1-text_height-6), (x1+text_width-6, y1), color, -1)
            elif pil['sub_class1'][:3] == 'fix':
                if  pil['sub_class2'][:3] == 'lig':
                    pil_text = pil['sub_class2'][:3]
                    (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
                    cv2.rectangle(overlay, (x2, y1), (x2+text_width, y1+text_height+13), color, -1)
                else:
                    pil_text = pil['sub_class2'][:3]
                    (text_width, text_height) = cv2.getTextSize(pil_text, font, fontScale=1, thickness=1)[0]
                    cv2.rectangle(overlay, (x1, y1-text_height-6), (x1+text_width, y1), color, -1)

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
 
def readfiles(path, Ext):
    file_dict = defaultdict(str)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext == ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)
                
                file_dict[filename] = file_path
    
        return file_dict

        
def MakeOutputPath(dir, path, savedir):
    root, file = os.path.split(path)    
    filename, ext = os.path.splitext(file)
    mid = '\\'.join(root.split('\\')[len(dir.split('\\')):])
    folder = os.path.join(savedir, mid)
    os.makedirs(folder,  exist_ok=True) 
    output_path = os.path.join(folder, f'{filename}{ext}')
    return output_path


_, json_dir, img_dir, save_img_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.png')
json_dict= readfiles(json_dir, '.json')

# 이미지 시각화 작업
vis_error_list = []
for filename, img_path in tqdm(img_dict.items(), desc='시각화'):
    
    json_path = json_dict[filename]

    output_img_path = os.path.join(save_img_dir, f'{filename}.png')
    
    logger.info(img_path)
    
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)

    if not json_file:
        shutil.copy2(img_path, output_img_path)
    
    else:
        img = Image.open(img_path)
        
        fontpath = "malgunbd.ttf"
        
        numpy_image = np.array(img)
        cv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        overlay = cv_image.copy()
        
        text_background(json_file['objects'])    # 텍스트 백그라운드 시각화
        
        # 백그라운드 투명도 조절
        alpha = 0.7
        img = cv2.addWeighted(cv_image, alpha, overlay, 1-alpha, 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        
        font = ImageFont.truetype(fontpath, 15)
        sub_font = ImageFont.truetype(fontpath, 5)
        draw = ImageDraw.Draw(img)
        d = DashedImageDraw(img)
        
        visualization(json_file['objects'])   # 텍스트, bbox 시각화
        legend()    # 범례 시각화

        img.save(output_img_path, 'png')

if len(vis_error_list) > 0:
    df = pd.DataFrame(vis_error_list, columns=['filename', 'coordinates'])
    df.to_excel('./vis_error.xlsx', index=False)