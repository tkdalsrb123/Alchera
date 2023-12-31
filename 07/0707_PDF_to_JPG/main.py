from pdf2image import convert_from_path
import os, sys
import pandas as pd

_, pdf_dir, save_dir = sys.argv

pdf_page_list = []
for root, dirs, files in os.walk(pdf_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.pdf':
            pdf_path = os.path.join(root, file)
            print(pdf_path, 'read pdf!!!')
            
            mid = '\\'.join(root.split('\\')[len(pdf_dir.split('\\')):])
            folder = os.path.join(save_dir, mid)
            os.makedirs(folder, exist_ok=True)
            save_img_path = os.path.join(folder, filename)
            
            pages = convert_from_path(pdf_path, dpi=300, poppler_path=r'.\Release-23.05.0-0\poppler-23.05.0\Library\bin')
            
            pdf_page_list.append([mid, file, len(pages)])
            # pdf 페이지 별로 jpg로 저장
            for i, page in enumerate(pages):
                num = f'{i+1}'.rjust(3,'0')
                save_img = f'{save_img_path}_{num}.jpg'
                page.save(save_img, 'JPEG')
                print(save_img, 'image down!!!')

df = pd.DataFrame(pdf_page_list, columns=['category', 'pdf 파일명', '페이지 수'])
df.to_excel('./pdf_page.xlsx', index=False)