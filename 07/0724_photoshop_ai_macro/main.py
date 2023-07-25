from pywinauto.application import Application
from pywinauto import findwindows
from pywinauto

# procs = findwindows.find_elements()

# for proc in procs:
#     print(proc, proc.process_id)

app = Application(backend="uia")
app.connect(path = r"C:\Program Files\Adobe\Adobe Photoshop (Beta)\Photoshop.exe")

dlg = app['Notepad']
dlg = app.top_window()
dlg = app.ChildWindow
# dlg.print_control_identifiers()
# dlg['메뉴 모음']['파일(F)'].click()
