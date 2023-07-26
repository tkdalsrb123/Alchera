from pywinauto.application import Application
from pywinauto import findwindows
from pywinauto.controls.common_controls import ToolbarWrapper
import time
from pywinauto import mouse
from pywinauto.keyboard import SendKeys, KeySequenceError
import win32api
from pywinauto.controls.menuwrapper import MenuItem
from pywinauto.controls.hwndwrapper import HwndWrapper

# procs = findwindows.find_elements()

# for proc in procs:
#     print(proc, proc.process_id)

app = Application(backend="uia").connect(path=r"C:\Program Files\Adobe\Adobe Photoshop (Beta)\Photoshop.exe")


# mouse control
dlg = app['Dialog']
# dlg['최대화'].click()
mouse.click(button='left', coords=(52, 13))
time.sleep(1)
mouse.click(button='left', coords=(60, 50))
time.sleep(1)
mouse.double_click(button='left', coords=(230, 220))
time.sleep(1)
mouse.press(button='left', coords=(169, 265))
time.sleep(2)
mouse.move(coords=(275, 330))
time.sleep(1)
mouse.release(button='left', coords=(275, 330))
time.sleep(1)
for i in range(130):
    SendKeys('+{RIGHT}')
for i in range(60):
    SendKeys('+{DOWN}')
time.sleep(1)
mouse.click(button='left', coords=(910, 754))
time.sleep(1)
app['Dialog']['Pane'].type_keys("korea wild boar{ENTER}", with_spaces=True)
time.sleep(30)
mouse.click(button='left', coords=(52, 13))
time.sleep(1)
mouse.click(button='left', coords=(125, 328))
time.sleep(1)
mouse.click(button='left', coords=(345, 360))
time.sleep(1)
SendKeys('{ENTER}')
# app['Dialog'].print_control_identifiers()