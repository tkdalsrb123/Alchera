from pywinauto.application import Application
from pywinauto import findwindows

# procs = findwindows.find_elements()

# for proc in procs:
#     print(proc, proc.process_id)

app = Application(backend="uia")
app.connect(path = r"C:\Program Files\Adobe\Adobe Photoshop (Beta)\Photoshop.exe")

dlg = app['Notepad']
dlg = app.top_window()
dlg['파일(F)'].select()
# dlg.print_control_identifiers()
# dlg['메뉴 모음']['파일(F)'].click()
