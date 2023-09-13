import pandas as pd
import os, sys, json


_, excel_dir, output_dir = sys.argv

excel = pd.read_excel(excel_dir)

