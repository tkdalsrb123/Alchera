import json, cv2, os, sys
import pandas as pd
from collections import defaultdict
import googletrans
import logging
from tqdm import tqdm

def readfiles(dir):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.mp4':
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    
    return file_dict

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
_, csv_dir, video_dir, output_dir = sys.argv

logger = make_logger('log.log')
mp4_dict = readfiles(video_dir)

df = pd.read_csv(csv_dir, encoding='utf-8')

translator = googletrans.Translator()

for i in tqdm(range(0, df.shape[0], 5)):
    filename = df.loc[i, '파일명']
    logger.info(filename)
    date = df.loc[i, '날짜']
    sub_category = translator.translate(df.loc[i, '장소'], dest='en').text
    activity = translator.translate(df.loc[i, '활동'], dest='en').text
    source = df.loc[i, '출처']
    composition = df.loc[i, '촬영구도']
    location = df.loc[i, '장소.1']
    audio = df.loc[i, '오디오 유뮤']
    time = df.loc[i, '시간대']
    person = df.loc[i, '사람']
    kor_list = []
    for j in range(5):
        kor_list.append(df.loc[i+j, '캡션(kor)'])
    
    mp4_path = mp4_dict[filename]
    cap = cv2.VideoCapture(mp4_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    totlaNoFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = totlaNoFrames // fps
    
    duration = durationInSeconds
    
    eng_list = [translator.translate(sen, dest='en').text for sen in kor_list]

    word_per_list = [len(sen.split(' ')) for sen in eng_list]

    json_tree = {
        "videos":[
            {
            "filename":f'{filename}.mp4', 
            "duration":duration, 
            "sub-category":sub_category, 
            "activity":activity, 
            "source":source, 
            "composition":composition, 
            "location":location, 
            "audio":audio, 
            "time":time, 
            "person_present":person, 
            "kor_sentences":kor_list, 
            "eng_sentences":eng_list, 
            "words_per_sentence":word_per_list, 
            "total_sentences": 5
            }
        ]
}

    output_json_path = os.path.join(output_dir, f'{filename}.json')
    with open(output_json_path, 'w', encoding='utf-8') as out:
        json.dump(json_tree, out, indent=2, ensure_ascii=False)
    
    