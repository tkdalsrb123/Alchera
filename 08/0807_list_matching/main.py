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

_, input_dir, csv_dir, output_dir = sys.argv

all_df = pd.DataFrame(columns=['name', 'duration', 'url', 'search_sum', 'revise', 'match'])
csv_list = os.listdir(csv_dir)
for csv_file in csv_list:
    filename, ext = os.path.splitext(csv_file)
    if ext == '.csv':
        csv_path = os.path.join(csv_dir, csv_file)
        
        csv_file = pd.read_csv(csv_path, encoding='utf-8')
        
        csv_file['revise'] = csv_file['name'].apply(set_file_name)
        csv_file['match'] = csv_file['revise'].str.replace(' ', '')

        all_df = pd.concat([all_df, csv_file], ignore_index=True)

output_df = pd.DataFrame(columns=['revise', 'duration', 'url', 'search_sum'])
mp4_list = os.listdir(input_dir)
for mp4_file in mp4_list:
    filename, ext = os.path.splitext(mp4_file)
    filename = filename.replace(' ', '')
    if ext == '.mp4':
        match_df = all_df.loc[all_df['match'] == filename, ['duration', 'url', 'search_sum', 'revise']]
        if match_df.shape[0] == 2:
            print(filename)
        output_df = pd.concat([output_df, match_df], ignore_index=True)
        
output_df.drop_duplicates(subset='url', inplace=True)
output_df.to_csv(f'{output_dir}/matcing_file.csv', encoding='utf-8-sig', index=False)
# all_df.to_csv(f'{output_dir}/all_file.csv', encoding='utf-8-sig', index=False)
        