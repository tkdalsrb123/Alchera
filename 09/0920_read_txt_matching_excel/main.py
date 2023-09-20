import sys, os
import pandas as pd
from collections import deque
import logging
from tqdm import tqdm

def make_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # formatter
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s:%(lineno)d] -- %(message)s")
    # file_handler
    file_handler = logging.FileHandler(log, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    # logger.add
    logger.addHandler(file_handler)
    
    return logger

keyword = [
"떨어짐",
"넘어짐",
"깔림",
"부딪힘",
"맞음",
"무너짐",
"끼임",
"절단 베임 찔림",
"감전",
"폭발 파열",
"화재",
"불균형 및 무리한 동작",
"이상온도 물체접촉",
"화학물질 누출 접촉",
"사고_기타",
"진폐",
"중독",
"난청",
"요통",
"질병_기타"
]

def deq(x):
    x_split = []
    for i in x.split('/'):
        if i.strip() not in keyword:
            x_split.append(f'{i} 0')
        else:
            x_split.append(i)
    v = deque(x_split)
    v.appendleft(x)
    key_list.append(v)

_, excel_dir, output_dir = sys.argv

logger = make_logger('log.log')

excel_list = os.listdir(excel_dir)

for excel_name in tqdm(excel_list):
    excel_path = os.path.join(excel_dir, excel_name)

    excel = pd.read_excel(excel_path)

    key_list = []
    excel.iloc[:, 0].apply(deq)


    df = pd.DataFrame(key_list)

    df.to_excel(f'{output_dir}/{excel_name}', index=False)
