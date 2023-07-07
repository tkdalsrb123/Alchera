import sys
import pandas as pd
from tqdm import tqdm

_, excel_dir, save_dir = sys.argv

# 엑셀파일에서 시트별로 불러오기
input1 = pd.read_excel(excel_dir, sheet_name=0)
input2 = pd.read_excel(excel_dir, sheet_name=1)

# 하나의 속성을 key값으로 두고 value값에 해당 속성의 단어가 Series로 들어간 dict
group = dict(list(input2.groupby('속성')['단어']))

df_raw_list = []
for idx in tqdm(range(input1.shape[0])):
    property = input1.loc[idx]['속성']
    property_group = group[property].tolist()   # input1에 속성값인 group에 key값의 단어들을 리스트 형태로 불러옴
    
    df = input1.loc[idx].copy()
    sample_df = input1.loc[idx].copy()
    lower_sentence = input1.loc[idx]['문장'].lower()
    sample = input1.loc[idx]['문장']
    
    # 불러온 속성의 value들을 문장과 하나씩 매칭하기
    for i in property_group:
        word = i.lower()
        if word in lower_sentence:    # 단어가 해당 문장에 있을 경우
            if sample == df['문장']:    # 매칭된 단어가 없어 변경이 되지 않았을 경우
                if lower_sentence.count(word) == 1:    # 문장에 단어가 한개일 경우
                    df['문장'] = sample.replace(i, f'${i}$')    
                    df_raw_list.append(df)
                else:
                    index = -1
                    while True:     # 한 개 이상일 경우 중복되지 않게 한 문장을 여러 문장으로 전처리하여 생성
                        index = lower_sentence.find(word, index+1)     # 단어의 인덱스를 찾는다. 찾는 문자가 존재하면 해당 위치의 index를 반환, 존재하지 않다면 -1을 반환
                        if index == -1: 
                            break
                        df['문장'] = sample[:index] + sample[index:index+len(i)].replace(i, f'${i}$') + sample[index+len(i):]   # 문장의 단어를 전처리하여 저장 
                        df2 = df.copy()
                        df_raw_list.append(df2)
                        
            else:   # 매칭된 단어가 존재해 변경이 되었을 경우
                if lower_sentence.count(word) == 1:
                    sample_df['문장'] = sample.replace(i, f'${i}$')
                    sample_df2 = sample_df.copy()
                    df_raw_list.append(sample_df2)
                else:
                    index = -1
                    while True:
                        index = lower_sentence.find(word, index+1)
                        if index == -1:
                            break
                        sample_df['문장'] = sample[:index] + sample[index:index+len(i)].replace(i, f'${i}$') + sample[index+len(i):]
                        sample_df2 = sample_df.copy()
                        df_raw_list.append(sample_df2)

    # 문장에 매칭 단어가 없을 경우
    if input1.loc[idx]['문장'] == df['문장']:
        df['문장'] = '$T$ ' + df['문장']
        df_raw_list.append(df)


raw_df = pd.DataFrame(df_raw_list)
raw_df = raw_df.sort_values('key값')


raw_df.to_excel(f'{save_dir}/new.xlsx', index=False)


