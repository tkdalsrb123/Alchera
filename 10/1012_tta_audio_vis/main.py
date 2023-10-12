import os, sys, json, logging
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import librosa
import wave
from scipy.io import wavfile
import numpy as np
from tqdm import tqdm
from collections import defaultdict

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

def readfiles(dir, Ext):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    return data

def io_file(file, label):
    filename = os.path.splitext(file)[0]
    file_path = wav_dict[filename]
    output_file_path = makeOutputPath(file_path, input_dir, output_dir, '.png')
    x, sr = librosa.load(file_path)
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(10,5))
    plt.title(label)
    librosa.display.specshow(Xdb, sr = sr, x_axis = 'time', y_axis = 'hz')
    plt.colorbar(format = "%+2.f dB")
    plt.savefig(output_file_path)
        
    
_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

wav_dict = readfiles(input_dir, '.wav')
json_dict = readfiles(input_dir, '.json')

for filename, json_path in tqdm(json_dict.items()):
    json_file = readJson(json_path)
    logger.info(json_path)
    inside_filename = json_file['audio_inside_info']['audio_inside_file_name']
    inside_label = json_file['audio_inside_info']['audio_inside_label']
    outside_filename = json_file['audio_outside_info']['audio_outside_file_name']
    outside_label = json_file['audio_outside_info']['audio_outside_label']
    io_file(inside_filename, inside_label)
    io_file(outside_filename, outside_label)