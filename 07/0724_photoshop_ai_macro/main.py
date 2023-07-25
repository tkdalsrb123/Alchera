from pywinauto.application import Application
from pywinauto import findwindows
from pywinauto.controls.common_controls import ToolbarWrapper
import time
from pywinauto import mouse
import win32api

# procs = findwindows.find_elements()

# for proc in procs:
#     print(proc, proc.process_id)

# x, y = win32api.GetCursorPos()
app = Application(backend="uia").connect(path = r"C:\Program Files\Adobe\Adobe Photoshop (Beta)\Photoshop.exe")


dlg = app['Dialog']
dlg['최대화'].click()
mouse.click(button='left', coords=(80, 200))
time.sleep(1)
mouse.double_click(button='left', coords=(250, 200))
time.sleep(1)
# app.dlg.print_control_identifiers()
# print(app.dlg.print_control_identifiers())

# app.Dialog.menu_select('파일(F)')
# app.Dialog.파일(F).Open.Edit.SetEditText(r"C:\Users\Alchera115\wj.alchera\Alchera_data\07\0724_photoshop_ai_macro\축사피해-로드뷰\축사피해-로드뷰\로드뷰_경남 고성군 개천면 - 2023-07-18T194546.145.png")
# app['Dialog']['메뉴 모음'].print_control_identifiers()
# dlg['메뉴 모음']['파일(F)'].child_window(title='파일(F)', control_type="MenuItem").select()
# dlg.print_control_identifiers()
# time.sleep(1)
# ToolbarWrapper.menu_bar_click_input(menu)
# app.dlg.child_window(title='메뉴 모음', control_type='MenuBar')
# dlg.print_control_identifiers()
# dlg['메뉴 모음']['파일(F)'].click()

