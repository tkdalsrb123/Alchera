import os, sys
import pandas as pd

_, input_dir, output_dir = sys.argv


df_list = []
i = 1
for root, dirs, files in os.walk(input_dir):
    for file in files:
        root1, filename_jpg = os.path.split(root)
        root2, Type = os.path.split(root1)
        filename_pdf = filename_jpg.split('_')[0]
        
        df_list.append([i , filename_pdf, filename_jpg, file, Type, root])
        
        i += 1
        
df = pd.DataFrame(df_list, columns=['No', 'filename_pdf', 'filename_jpg', 'crop_img_name', 'type', '저장 파일 경로'])
df.to_excel(f'{output_dir}/file.xlsx', index=False)