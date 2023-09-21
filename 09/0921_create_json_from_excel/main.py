import os, sys, json
import pandas as pd

def makejson(x):
    id = x['id']
    gender = x['gender']
    age = x['age']
    

_, excel_dir, output_dir = sys.argv

excel = pd.read_excel(excel_dir)
excel['id']