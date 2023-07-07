import pandas as pd
import os, sys

_, csv_dir, output_dir = sys.argv

concat_df = pd.DataFrame(columns=['사이트', '종류', '제품명', '가격', '링크'])
for root, dirs, files in os.walk(csv_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.csv':
            csv_path = os.path.join(root, file)
            
            df = pd.read_csv(csv_path)

            for i in range(0, df.shape[1], 3):
                category_df = df.iloc[:, i:i+3].copy()
                category_df['종류'] = '_'.join(category_df.columns[0].split('_')[:-1])
                category_df['사이트'] = filename
                category_df.columns = ['제품명', '가격', '링크', '종류', '사이트']
                concat_df = pd.concat([concat_df, category_df])
concat_df = concat_df.dropna()
concat_df.to_csv(f'{output_dir}/all_rank.csv', index=False)
