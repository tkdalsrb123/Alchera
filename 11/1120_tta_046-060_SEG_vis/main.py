import os, sys, cv2, json, logging
import numpy as np
from PIL import Image, ImageDraw
from label import label
from tqdm import tqdm
from collections import defaultdict
import math

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

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
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

categories = {
       1  : "아스팔트 도로파임",
    
       2 : "콘크리트 도로파임",
    
       3 : "종방향균열",
   
       4 : "횡방향균열",
   
       5 : "거북등균열",
   
       6 : "줄눈부파손",
   
       7 : "십자파손",
   
       8 : "절삭보수부파손",
   
       9 : "긴급보수부파손",
   
       10 : "응력완화줄눈 화살표",
   
       11 : "응력완화줄눈 오각형",
   
       12 : "응력완화줄눈 삼각형",
   
       13 : "응력완화줄눈",
   
       14 : "신축이음부",
   
       15 : "차선",
   
       16 : "규제봉",
   
       17 : "맨홀",

       18 : "배수로" }
 

if __name__ == '__main__':
    _, img_dir, json_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    img_dict = readfiles(img_dir, '.jpg')
    json_dict = readfiles(json_dir, '.json')
    
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        cat = filename.split('_')[2]
        unique = filename.split('_')[3]
        img_path = img_dict[filename]

        output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'jpg')
        data = readJson(json_path)
        img = read_img(img_path)
        
        annotations = data['annotations']

        if type(annotations) == dict:
            annotations = [annotations]
        
        if unique in ['04', '05']:
            for ann in annotations: 
                category_id = ann['category_id']
                seg = ann.get('segmentation')
                category = categories.get(category_id)
                
                if seg:
                    points = [(round(seg[i]), round(seg[i+1])) for i in range(0, len(seg), 2)]
                    points = np.array(points, np.int32)
                    cv2.polylines(img, [points], isClosed=True, color=(0, 0, 255), thickness=3)
                    if category:
                        img = label(img, category, 20, (255, 0, 0), points[0], 0.5)

        elif unique in ['01', '02', '03', '06']:
            for ann in annotations: 
                category_id = ann['category_id']
                bbox = ann.get('bbox')
                category = categories.get(category_id)
                
                if bbox:
                    x1 = round(bbox[0])
                    y1 = round(bbox[1])
                    x2 = x1 + round(bbox[2])
                    y2 = y1 + round(bbox[3])
                    cv2.rectangle(img, (x1,y1), (x2, y2), color=(0, 0, 255), thickness=3)
                    if category:
                        img = label(img, category, 20, (255, 0, 0), (x1, y2), 0.5)
        
  
        if cat == 'F':
            img = Image.fromarray(img)
            d = DashedImageDraw(img)
            d.dashed_rectangle(((0,699),(2448, 1349)), dash=(7,5), outline=(0,0,255), width=3)
            img = np.array(img)
            
        elif cat == 'V':
            cv2.rectangle(img, (50, 50), (1998, 1998), color=(0, 0, 255), thickness=3)

        save_img(output_img_path, img, 'jpg')
        logger.info(output_img_path)