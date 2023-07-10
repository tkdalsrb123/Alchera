import os, sys
import pandas as pd
from PIL import Image, ImageFont, ImageDraw

_, image_dir, csv_dir, save_dir = sys.argv

df = pd.read_csv(csv_dir)

for root, dirs, files in os.walk(image_dir):
    if len(files) > 0:
        if os.path.splitext(files[0])[-1] == '.jpg':
            file_list = [file for file in files if os.path.splitext(file)[-1] == '.jpg']
            file_list = sorted(file_list, key=lambda x: int(x[:-4]))    # 이미지 파일 번호 순으로 정렬
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
                    
                    # 이미지 파일 번호와 csv에 파일 순서로 매칭
                    if int(filename)-1 < select_df.shape[0]:
                        select_df = select_df.sort_values('index')
                        text1 = select_df.iloc[int(filename)-1, 2]
                        text2 = select_df.iloc[int(filename)-1, 3]
                        
                        img = Image.open(img_path)
                        
                        # 이미지 색상 변경
                        if img.mode == 'RGBA':
                            img = img.convert('RGB')
                        elif img.mode == 'P':
                            img = img.convert('RGB')
                            
                        fontpath = "fonts/gulim.ttc"
                        font = ImageFont.truetype(fontpath, 13)
                        draw = ImageDraw.Draw(img)
                        
                        _, _, w1, h1 = font.getbbox(text1)
                        h = 0
                        
                        left, top, right, bottom = draw.textbbox((0, 0),text1, font=font)
                        draw.rectangle((left, top ,right, bottom), fill='black')    # text background
                        draw.text((0,0), text1, font=font, fill='white')
                        
                        for idx in range(0, len(text2), len(text2)//4):
                            left, top, right, bottom = draw.textbbox((w1+2,h),text2[idx:idx+len(text2)//4], font=font)
                            draw.rectangle((left, top ,right, bottom), fill='black')
                            draw.text((w1+2,h), text2[idx:idx+len(text2)//4], font=font, fill='white')
                            h += h1

                        img.save(save_img, 'jpeg')
                        print(save_img,'저장!!!')
                
            
            
            