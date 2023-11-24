import os, sys, shutil
import pandas as pd

def processing(x):
    ID = x['대화 생성ID']
    sen_id = x['문장ID']
    per = x['대화자']
    form = x['form']
    val = x.iloc[6:].values
    
    pne_list = []
    
    for i in range(0, len(val), 2):
        if type(val[i]) == str:
            pne_class_list.append([val[i+1], val[i]])
            pne_list.append([val[i], val[i+1]])
    print(form)
    for pne in pne_list:
        if pne[0] not in form:
            typo_list.append([ID, sen_id, per, form, pne[0], pne[1]])

if __name__ == "__main__":
    _, excel_dir, output_dir = sys.argv

    root, file = os.path.split(excel_dir)
    shutil.copy2(excel_dir, f'{output_dir}/{file}')
    
    df = pd.read_excel(excel_dir)
    pne_class_list = []
    typo_list = []
    df.apply(processing, axis=1)
    
    
    sheet2 = pd.DataFrame(pne_class_list, columns=['Class', 'PNE'])
    sheet3 = pd.DataFrame(typo_list, columns=['대화 생성ID', '문장ID', '대화자', 'form', 'PNE', 'Class'])
    
    
    with pd.ExcelWriter(f'{output_dir}/{file}', mode='a', engine='openpyxl') as w:
        sheet2.to_excel(w, index=False, sheet_name='Sheet2')
        sheet3.to_excel(w, index=False, sheet_name='오탈자')