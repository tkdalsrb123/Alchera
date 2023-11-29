import pandas as pd

def change(text):
    if '+' in text:
        ts = text.split('+')
        ts = [category.get(i) for i in ts]
        text = '+'.join(ts)

    else:   
        t = category.get(text)
        if t:
            text = t
    
    return text

def preprocsessing(x):
    name = '_'.join([change(x['촬영구분']), change(x['공간유형']), change(x['배경타입']), change(x['조명타입']), change(x['조명색'])])
    name_dict[name] = str(x['시나리오넘버']).zfill(3)
    
category = {
"실내":"indoor",
"실외":"outdoor",
"단순":"SB",
"순광":"PL",
'역광':"BL",
"백색":"WL",
"주백색":"D",
"네온":"N",
"자연광":"NL",
"복잡":"CB",
"햇빛있음":"T",
"햇빛없음":"F",
"버스정류장":"Bus",
"가로등":"Steetlight",
"편의점":"Store",
"주간":"Day",
"야간":"Night"}

path = r"C:\Users\Alchera115\Downloads\라이브니스시나리오.xlsx"
df = pd.read_excel(path)
name_dict = {}
df.apply(preprocsessing, axis=1)

print(name_dict)