import os, sys, logging, json
import textwrap
from tqdm import tqdm
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

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

def makeOutputPath(file_path, file_dir, output_dir, Ext, filename):
    root, file = os.path.split(file_path)
    # filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_text_size(draw, text, font):
    text_bbox = draw.textbbox((0,0), text, font=font)
    h = text_bbox[3] - text_bbox[1]
    w = text_bbox[2] - text_bbox[0]
    
    return h, w
    
if __name__ == '__main__':
    _, source_dir, label_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    source_dict = readfiles(source_dir, '.json')
    label_dict = readfiles(label_dir, '.json')
    
    for filename, source_path in tqdm(source_dict.items()):
        logger.info(source_path)
        
        label_path = label_dict[filename]
        logger.info(label_path)
        
        source_data = readJson(source_path)
        label_data = readJson(label_path)

        documentid = source_data['dataset']['documentId']
        abstract = source_data['dataset']['abstract']
        claims = source_data['dataset']['claims']
        sno = label_data['dataset']['Sno']
        stext = label_data['dataset']['Stext']
        
        output_filename = f'{sno}_{stext}_{documentid}'
        output_img_path = makeOutputPath(label_path, label_dir, output_dir, 'png', output_filename)
                        
        text_list = [['발명의 요약', abstract], ['정구항', claims], ['소분류 코드', sno], ['소분류 설명', stext]]

        canvas_size = (1200, 1200)  # image size
        key_font_size = 15      # key font size
        value_font_size = 10    # value font size
        text_length = 120    # text length
        
        img = Image.new('RGB', canvas_size, "white")
        key_font = ImageFont.truetype('C:\Windows\Fonts\HMKMRHD.TTF', key_font_size)
        value_font = ImageFont.truetype('C:\Windows\Fonts\H2GTRM.TTF', value_font_size)
        draw = ImageDraw.Draw(img)

        x = 5
        y = 5
        for text in text_list:
            key_h, key_w = get_text_size(draw, text[0], key_font)
            val_h, val_w = get_text_size(draw, text[1], value_font)
            draw.text((x, y), text[0], (0, 0, 255), font=key_font)
            if val_w > canvas_size[0]:
                lines = textwrap.wrap(text[1], width=text_length)
                for line in lines:
                    y += key_h + val_h -5
                    draw.text((x, y), line, (0, 0, 0), font=value_font)
                y += key_h + val_h + 20
            else:
                draw.text((x, y+key_h+5), text[1], (0, 0, 0), font=value_font)
                y += key_h + val_h + 20
        
        img.save(output_img_path, 'PNG')
        logger.info(output_img_path)
            
            
        