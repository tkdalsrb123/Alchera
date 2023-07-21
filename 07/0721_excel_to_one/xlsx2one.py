import pandas as pd
import os, sys
import traceback
from tqdm import tqdm

_, input_dir, output_dir = sys.argv

data_list = []
for root, dirs, files in os.walk(input_dir):
    for file in tqdm(files):
        filename, ext = os.path.splitext(file)
        if ext == '.xlsx' or ext == '.xlsm':
            xlsx_path = os.path.join(root, file)
            print(xlsx_path)
            
            summary = pd.read_excel(xlsx_path, sheet_name='항목 및 결과 요약표', header=None)
            excel = pd.read_excel(xlsx_path, sheet_name=None, header=None)
            sheet_names = excel.keys()
            
            try:
                for idx in range(summary.shape[0]):
                    raw = summary.iloc[idx]
                    raw = raw.dropna()
                    x_list = raw.tolist()
                    
                    if len(x_list) > 4:
                        # 데이터 번호, 데이터 명 추출
                        if len(x_list) == 6 and '데이터명' in x_list:   
                            data_num = x_list[1]
                            data_name = x_list[3]
                        

                        elif type(x_list[2]) == int:
                            # 검사 결과값이 있을 경우
                            if type(x_list[-1]) == float or type(x_list[-1]) == int:
                                tc = f'TC{x_list[2]} 검사이력'
                                data_type = x_list[3]
                                evalution_type = x_list[-2]
                                evalution_result = x_list[-1]
                                
                                # 해당 TC 시트에서 라벨링 유형 추출
                                for name in sheet_names:
                                    strip_name = name.strip()
                                    if tc == strip_name:
                                        in_summary = pd.read_excel(xlsx_path, sheet_name=name, header=None)
                                        for idx in range(in_summary.shape[0]):
                                            raw = in_summary.iloc[idx]
                                            raw = raw.dropna()                    
                                            i_list = raw.tolist()
                                            si_list = [i.strip() for i in i_list if type(i) == str]
                                            if '어노테이션 타입' in si_list or '라벨링 유형' in si_list:
                                                label_type = i_list[1]
                                    
                                                data_list.append([data_num, data_name, label_type, data_type, evalution_type, evalution_result])

                            else:   #  검사 결과 값이 N/A 값일 경우
                                tc = f'TC{x_list[2]} 검사이력'
                                data_type = x_list[3]
                                evalution_type = x_list[-1]
                                evalution_result = 'N/A'
                                
                                for name in sheet_names:
                                    strip_name = name.strip()
                                    if tc == strip_name:
                                        in_summary = pd.read_excel(xlsx_path, sheet_name=tc, header=None)
                                        for idx in range(in_summary.shape[0]):
                                            raw = in_summary.iloc[idx]
                                            raw = raw.dropna()                    
                                            i_list = raw.tolist()
                                            si_list = [i.strip() for i in i_list if type(i) == str]

                                            if '어노테이션 타입' in si_list or '라벨링 유형' in si_list:
                                                label_type = i_list[1]
                                    
                                                data_list.append([data_num, data_name, label_type, data_type, evalution_type, evalution_result])

            except ValueError:
                print('데이터 오류!!!')
                print(traceback.format_exc())
                
df = pd.DataFrame(data_list, columns=['과제 데이터번호', '데이터명', '라벨링 유형', '검사항목', '측정지표', '검사 결과'])

df.to_excel(f'{output_dir}/xlsx2one.xlsx', index=False)


