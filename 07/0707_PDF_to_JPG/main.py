from pdf2image import convert_from_path
import os, sys

_, pdf_dir, save_dir = sys.argv

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
            
            # pdf 페이지 별로 jpg로 저장
            for i, page in enumerate(pages):
                save_img = f'{save_img_path}_{i+1}.jpg'
                page.save(save_img, 'JPEG')
                print(save_img, 'image down!!!')