import os, sys
import pandas as pd
from PIL import Image, ImageFont, ImageDraw

_, image_dir, csv_dir, save_dir = sys.argv

df = pd.read_csv(csv_dir)

for root, dirs, files in os.walk(image_dir):
    if len(files) > 0:
        if os.path.splitext(files[0])[-1] == '.jpg':
            file_list = [file for file in files if os.path.splitext(file)[-1] == '.jpg']
            file_list = sorted(file_list, key=lambda x: int(x[:-4]))
            for file in file_list:
                filename, ext = os.path.splitext(file)
                if ext == '.jpg':
                    mid = '\\'.join(root.split('\\')[len(image_dir.split('\\')):])
                    folder = os.path.join(save_dir, mid)
                    os.makedirs(folder, exist_ok=True)
                    save_img = os.path.join(folder, file)
                    root_split = root.split('\\')
                    
                    site, category = root_split[-2].replace('_image', ''), root_split[-1]
                    img_path = os.path.join(root, file)
                    print(img_path, '시각화!!')
                    select_df = df[(df['사이트'] == site) & (df['종류'] == category)].reset_index()
                    
                    if int(filename)-1 < select_df.shape[0]:
                        select_df = select_df.sort_values('index')
                        text = ' '.join(select_df.iloc[int(filename)-1, 2:4].tolist())
                        
                        img = Image.open(img_path)
                        fontpath = "fonts/gulim.ttc"
                        font = ImageFont.truetype(fontpath, 15)
                        draw = ImageDraw.Draw(img)
                    
                        draw.text((0,0), text, font=font, fill=(0,0,0))
                        
                        img.save(save_img, 'jpeg')
                        print(save_img,'저장!!!')
                
            
            
            