from pywinauto.application import Application
from pywinauto import findwindows

# procs = findwindows.find_elements()

# for proc in procs:
#     print(proc, proc.process_id)

app = Application(backend="uia")
app.start(r"C:\Program Files\Adobe\Adobe Photoshop (Beta)\Photoshop.exe")

dlg = app['Notepad']
# dlg = app.top_window()
app.dlg.print_control_identifiers()