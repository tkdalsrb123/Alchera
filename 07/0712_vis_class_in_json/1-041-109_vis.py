import json, os, sys
from PIL import Image, ImageFont, ImageDraw
from collections import defaultdict

_, input_dir, output_dir = sys.argv

img_dict = defaultdict(str)
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.jpg':
            img_path = os.path.join(root, file)
            img_dict[filename] = img_path

for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            img_path = img_dict[filename]
            mid_name, img_name = os.path.split(img_path)
            mid = '\\'.join(mid_name.split('\\')[len(input_dir.split('\\')):])
            folder = os.path.join(output_dir, mid)
            os.makedirs(folder, exist_ok=True)
            output_img_path = os.path.join(folder, img_name)
            
            with open(json_path, encoding='utf-8') as f:
                json_file = json.load(f)
            
            img = Image.open(img_path)
            fontpath = 'gulim.ttc'
            font = ImageFont.truetype(fontpath, 20)
            draw = ImageDraw.Draw(img)
            for ann in json_file['annotations']:
                cat_id = ann['category_id']
                text1 = [cat['name'] for cat in json_file['categories'] if cat['id'] == cat_id]
                gro_le = ann['growth_level']
                text2 = [gro['level_name'] for gro in json_file['growth_levels'] if gro['level_id'] == gro_le]
                text = '\n'.join([text1[0], text2[0]])
                points = [(point[0], point[1])for point in ann['keypoints']]
                draw.polygon(points, outline=(255,0,0), width=5)
                draw.text(points[0], text, font=font, fill=(255, 0, 0))
            
            img.save(output_img_path, 'png')
            print(output_img_path, '저장!!!')
