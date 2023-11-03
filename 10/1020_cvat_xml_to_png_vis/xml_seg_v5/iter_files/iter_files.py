
import os
from tqdm import tqdm
# from process_file import process_file

def iter_files(input_dir, exts):
    
    struct_dict = {}
    for roots, _, files in os.walk(input_dir):
        for file in files:
            basename, ext = os.path.splitext(file)
            if exts:
                if ext in exts:
                    struct_dict[basename] = os.path.join(roots, file)
            else:
                struct_dict[basename] = os.path.join(roots, file)


    return struct_dict

if __name__ == '__main__':
    color_files(r'.\sample_file\1. 원천데이터\1. 자갈 암석종류 분석 데이터',
    r'.\sample_file\2. 라벨링 데이터\1. 자갈 암석종류 분석 데이터', 0.0, './out')