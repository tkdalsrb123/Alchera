import json, os, sys, cv2, math
import pandas as pd
import numpy as np
from tqdm import tqdm
from PIL import ImageFont, ImageDraw, Image
import xmltodict
from collections import defaultdict

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

def legend():
    font = ImageFont.truetype(fontpath, 15)
    draw.text((0, 0), '■ vehicle', font=font,  fill=(000, 255, 000))
    draw.text((150, 0), '■ emergency', font=font, fill=(255, 000, 000))
    draw.text((300, 0), '■ vehicle_whole', font=font, fill=(225, 255, 000))
    draw.text((450, 0), '■ emergency_whole', font=font, fill=(255, 150, 0))
    draw.text((600, 0), '■ ptw', font=font, fill=(000, 255, 255))    
    draw.text((750, 0), '■ misc', font=font, fill=(51, 000, 255))
    draw.text((900, 0),  '--- 가림', font=font, fill=(255, 255, 255))
    draw.text((1050, 0), '....... 잘림', font=font, fill=(255, 255, 255))
    
def select_outline(Class):
    if Class == 'vehicle':
        return (000, 255, 000)
    elif Class == 'emergency':
        return (255, 000, 000)
    elif Class == 'vehicle_whole':
        return (225, 255, 000)
    elif Class == 'emergency_whole':
        return (255, 150, 0)
    elif Class == 'ptw':
        return (000, 255, 255)
    elif Class == 'misc':
        return (51, 000, 255)

def select_color(Class):
    if Class == 'vehicle':
        return (255, 000, 255)
    elif Class == 'emergency':
        return (255, 255, 255)
    elif Class == 'vehicle_whole':
        return (50, 50, 255)
    elif Class == 'emergency_whole':
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
            outline = select_outline(pil['class'])
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
            pil_text = pil['sub_class1'][:3] + '/' + pil['sub_class2'][:3]
            x1 = pil['xmin']
            y1 = pil['ymin']
            x2 = pil['xmin'] + pil['width']
            y2 = pil['ymin'] + pil['height']
            outline = select_outline(pil['class'])
            if pil['sub_class1'][:3] != 'fix':
                d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(7,5), outline=outline, width=1)
                draw.text((x1, y1-18), pil_text, font=font, fill=outline)
            elif pil['sub_class1'][:3] == 'fix':
                if pil['sub_class2'][:3] == 'lig':
                    pil_text = pil['sub_class2'][:3]
                    d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(7,5), outline=outline, width=1)
                    draw.text((x2, y1), pil_text, font=font, fill=outline)
                else:
                    pil_text = pil['sub_class2'][:3]
                    d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(7,5), outline=outline, width=1)
                    draw.text((x1, y1-15), pil_text, font=font, fill=outline)
        elif pil['truncation'] != '0':
            pil_text = pil['sub_class1'][:3] + '/' + pil['sub_class2'][:3]
            x1 = pil['xmin']
            y1 = pil['ymin']
            x2 = pil['xmin'] + pil['width']
            y2 = pil['ymin'] + pil['height']
            outline = select_outline(pil['class'])
            if pil['sub_class1'][:3] != 'fix':
                d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(1,1), outline=outline, width=1)
                draw.text((x1, y1-15), pil_text, font=font, fill=outline)
            elif pil['sub_class1'][:3] == 'fix':
                if pil['sub_class2'][:3] == 'lig':
                    pil_text = pil['sub_class2'][:3]
                    d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(1,1), outline=outline, width=1)
                    draw.text((x2, y1), pil_text, font=font, fill=outline)
                else:
                    pil_text = pil['sub_class2'][:3]
                    d.dashed_rectangle(((x1, y1),(x2, y2)), dash=(1,1), outline=outline, width=1)
                    draw.text((x1, y1-18), pil_text, font=font, fill=outline)

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
            color = select_color(pil['class'])
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
            color = select_color(pil['class'])
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
            color = select_color(pil['class'])
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

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

def makeinfo(x):
    info[x['filename']] = {'filename':x['filename'], 'date':x['date'], 'vehicle':x['vehicle']}

def json_tree(name, date, vehicle, project, objects):
    json_tree = {
    "file_name": name,
    "information": {
        "date": date,
        "vehicle": vehicle,
        "Collection_Partners": "MOBIS",
        "Label_Partners": "ALCHERA",
        "Project": project,
        "resolution_raw_width": "1280",
        "resolution_raw_heigth": "944",
        "resolution_gt_width": "768",
        "resolution_gt_height": "672"
    },
    'objects': objects}
    
    return json_tree
    
_, xml_dir, excel_dir, img_dir, save_dir = sys.argv

json_path_dict = defaultdict(str)

info = defaultdict(dict)
df = pd.read_excel(excel_dir)
df.apply(makeinfo, axis=1)  # excel 파일을 딕셔너리 형태로 변경

# xml 파일 -> json 파일
for root, dirs, files in os.walk(xml_dir):
    for file in files:
        ext = os.path.splitext(file)[-1]
        if ext == '.xml':
            xml_path = os.path.join(root, file)
            mid = '\\'.join(root.split('\\')[len(xml_dir.split('\\')):])
            folder = os.path.join(save_dir, mid)
            
            xml_file = readxml(xml_path)
            for img_info in xml_file['annotations']['image']:
                filename = os.path.split(img_info['@name'])[-1]
                
                if len(info[filename].keys()) != 0:     # excel 파일에 파일이 존재할 때
                    print(filename.replace('png', 'json'), '생성중!!!')
                    
                    info_file = info[filename]
                    date = info_file['date']
                    if 'N' in info_file['vehicle']:
                        vehicle = 'NQ5'
                    elif 'S' in info_file['vehicle']:
                        vehicle = 'Santafe'
                    elif 'A' in info_file['vehicle']:
                        vehicle = 'Sorento'
                    
                    if vehicle == 'NQ5' or vehicle == 'Santafe':
                        project = 'mobis_rir_2nd_eu'
                    elif vehicle == 'Sorento':
                        project = 'mobis_rir_2nd_na'
                    
                    list_object = []
                    for box_info in img_info['box']:
                        x = []
                        y = []
                        vehicle_class = box_info['@label']
                        x.append(float(box_info['@xtl']))
                        x.append(float(box_info['@xbr']))
                        y.append(float(box_info['@ytl']))                    
                        y.append(float(box_info['@ybr']))
                        x_min = min(x)
                        y_min = min(y)
                        x_max = max(x)
                        y_max = max(y)
                        x_cnt = np.median(x)
                        y_cnt = np.median(y)
                        width = max(x) - min(x)
                        height = max(y) - min(y)
                        for att_info in box_info['attribute']:
                            if att_info['@name'] == 'sub class 1':
                                subclass1 = att_info['#text']
                            elif att_info['@name'] == 'sub class 2':
                                subclass2 = att_info['#text']
                            elif att_info['@name'] == 'Stutation occlusion of box':
                                occlusion = att_info['#text']
                            elif att_info['@name'] == 'Stutation truncation of box':
                                truncation = att_info['#text']
                        
                        if occlusion == 'not occlusion' or occlusion == 'Both 2 wheel have no occlusion':
                            occlusion = '0'
                        elif occlusion == '1-50%occlusion' or occlusion == '1-25%occlusion' or occlusion == '1 wheel 100% visible, other wheel partially occlusion':
                            occlusion = '1'
                        elif occlusion == '25-50%occlusion' or occlusion == '1 wheel 100% occlusion, other wheel &lt; 50% occlusion':
                            occlusion = '2'
                            
                        if truncation == 'not truncation' or truncation == 'Both 2 wheel have no truncation':
                            truncation = '0'
                        elif truncation == '1-50%truncation' or truncation == '1-25%truncation' or truncation == '1 wheel 100% visible, other wheel partially truncation':
                            truncation = '1'
                        elif truncation == '25-50%truncation' or truncation == '1 wheel 100% truncation, other wheel &lt; 50% truncation':
                            truncation = '2'

                        list_object.append({'class':vehicle_class, 'sub_class1':subclass1, 'sub_class2':subclass2,
                                    'xmin':round(x_min), 'xmax':round(x_max), 'ymin':round(y_min), 'ymax':round(y_max), 'cnt_x':int(x_cnt), 'cnt_y':int(y_cnt), 
                                    'width':round(width), 'height':round(height), 
                                    'occlusion':occlusion, 'truncation':truncation})
                        
                    
                    
                    new_json = json_tree(filename, date, vehicle, project, list_object)
                    
                    os.makedirs(folder, exist_ok=True)
                    output_path = os.path.join(folder, filename.replace('png', 'json'))
                    
                    json_path_dict[filename] = output_path  # image와 매칭할 딕셔너리
                    with open(output_path, 'w', encoding='utf-8') as outfile:
                        json.dump(new_json, outfile, indent=2, ensure_ascii=False)
                
                else:
                    continue

# 이미지 시각화 작업
for root, dirs, files in os.walk(img_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.png':
            img_path = os.path.join(root, file)
            json_path = json_path_dict[filename]
            output_img_path = json_path.replace('json', 'png')
            
            with open(json_path, encoding='utf-8') as f:
                json_file = json.load(f)
            
            img = Image.open(img_path)
            
            fontpath = "NanumBarunGothicBold.ttf"
            
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
            draw = ImageDraw.Draw(img)
            d = DashedImageDraw(img)
            
            visualization(json_file['objects'])   # 텍스트, bbox 시각화
            legend()    # 범례 시각화

            img.save(output_img_path, 'png')
            print(f'{output_img_path} 시각화완료..!')
            
            