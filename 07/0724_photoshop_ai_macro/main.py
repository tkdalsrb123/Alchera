from pywinauto.application import Application
import time
from pywinauto import mouse
from pywinauto.keyboard import SendKeys
import os, sys

_, input_dir = sys.argv

file_len = len(os.listdir(input_dir))

app = Application(backend="uia").connect(path=r"C:\Program Files\Adobe\Adobe Photoshop (Beta)\Photoshop.exe")

file_coords = (60, 13)
start_generative_coords = (178, 273)
generative_coords = (283, 347)
make_generative_coords = (1151, 747)

for i in range(file_len):

    dlg = app['Dialog']
    # dlg['최대화'].click()
    mouse.click(button='left', coords=file_coords)     # 파일(F) 클릭

    mouse.click(button='left', coords=(file_coords[0], file_coords[1]+40))     # 열기(O) 클릭

    mouse.click(button='left', coords=(file_coords[0]+170, file_coords[1]+210))    # 이미지 클릭

    if i%7 >= 0:    # 7장 이후에 아래로 이동
        num = i//7
        for n in range(num):
            SendKeys('{DOWN}')
            
    for j in range(i%7):    # 불러오는 이미지 옆으로 이동
        SendKeys('{RIGHT}')
        
    SendKeys('{ENTER}')  # 이미지 엔터 후 열기

    mouse.press(button='left', coords=start_generative_coords)   # 생성형 범위 시작지점 잡기(이미지 좌측 위에 모서리)

    mouse.move(coords=generative_coords)   # 생성형 범위 끝지점으로 마우스 커서 이동

    mouse.release(button='left', coords=generative_coords)     # 생성형 범위 끝지점에서 마우스 놓기

    mouse.press(button='left', coords=generative_coords)   # 생성형 범위 끝지점 잡기

    mouse.move(coords=make_generative_coords)  # 생성형 생성 위치에 마우스 커서 이동

    mouse.release(button='left', coords=make_generative_coords)    # 생성형 생성 위치에 놓기

    mouse.click(button='left', coords=(make_generative_coords[0]-215, make_generative_coords[1]+30))   # 생성자 생성 클릭

    app['Dialog']['Pane'].type_keys("korea wild boar{ENTER}", with_spaces=True)     # 생성자 input 에 text 넣기
    time.sleep(20)
    
    mouse.click(button='left', coords=file_coords)     # 파일(F) 클릭

    mouse.click(button='left', coords=(file_coords[0], file_coords[1]+350))   # 내보내기 클릭

    mouse.click(button='left', coords=(file_coords[0]+285, file_coords[1]+350))   # png로 빠른 내보내기 클릭
    time.sleep(1)
    SendKeys('{ENTER}')     # 저장 폴더에 enter로 저장
