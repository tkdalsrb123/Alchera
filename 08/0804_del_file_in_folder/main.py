import pandas as pd
import os, sys

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

_, csv_dir, input_dir = sys.argv

df = pd.read_csv(csv_dir)

file_list = df[['name', 'execution']].to_dict(orient='records')

for file in file_list:
    filename = file['name']
    filename = set_file_name(filename)
    execution = file['execution']
    file_path = os.path.join(input_dir, f'{filename}.mp4')
    if execution == 'E':
        print(file_path, '삭제!!')
        os.remove(file_path)
    elif execution == 'H':
        rename = '보류_' + f'{filename}.mp4'
        file_rename_path = os.path.join(input_dir, rename)
        print(file_rename_path, '변형!!')
        os.rename(file_path, file_rename_path)

del_df = df[df['execution'] != 'E']
del_df['name'] = del_df['name'].apply(set_file_name)
csv_file = os.path.split(csv_dir)[-1]
del_df.to_csv(f'./{csv_file}', index=False)