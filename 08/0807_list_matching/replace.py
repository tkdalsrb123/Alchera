import os, sys
import pandas as pd

def set_file_name(video_title):
    file_name = []
    for word in video_title.split():
        new_word = []
        for char in word:
            if char.isalnum():
                new_word.append(char)
        file_name.append(''.join(new_word))
        
    file_name = ' '.join(file_name)
    return file_name


_, csv_dir, output_dir = sys.argv

filename = os.path.split(csv_dir)[-1]

df = pd.read_csv(csv_dir, encoding='utf-8-sig')
df['name'] = df['name'].apply(set_file_name)

df.to_csv(f'{output_dir}/Re_{filename}', encoding='utf-8-sig', index=False)
print(f'{output_dir}/Re_{filename}', '저장!!')