import os, sys
import pandas as pd
from collections import defaultdict, Counter

def readfiles(dir):
    file_dict = defaultdict(list)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.txt':
                file_path = os.path.join(root, file)

                file_dict[os.path.split(root)].append(file_path)
    return file_dict

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    txt_dict = readfiles(input_dir)
    
    dict2df = defaultdict(lambda: defaultdict(list))
    for unique, txt_path_list in txt_dict.items():
        for txt_path in txt_path_list:
            pass_text = ""
            error_text = ""
            root, file = os.path.split(txt_path)
            filename = file.split('_')[-1]
            with open(txt_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for l in lines:
                if 'Pass' in l:
                    pass_text = l.split(':')[1].replace('\n', '')
                elif '오류' in l:
                    error_text = l.split(':')[1]
            
            dict2df[filename]['pass/fail'].append(pass_text.strip())
            dict2df[filename]['error'].append(error_text.strip())
    
    list2df = []
    for filename, info in dict2df.items():
        pf_count = Counter(info['pass/fail'])
        if pf_count['o'] > pf_count['x']:
            text = 'pass'
        else:
            text = 'fail'
        error_text = '\n'.join(info['error'])
        list2df.append([filename, text, error_text])
    
    df = pd.DataFrame(list2df)
    df.to_excel(f'{output_dir}/text.xlsx', header=None, index=False)
        
        