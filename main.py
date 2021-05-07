# third party packages
import tkinter as tk

# local packages
from NPR.gui.detector import DetectorGUI
from NPR.gui.login import Login
from NPR.gui.show_data import ShowDataGUI
from NPR.ml_assets.plate_predictor import PlateRecognizer

# root window
root = tk.Tk()

# login window
# next window is initialize in gui/login.py
login_gui = Login(root)

# detector window
detector_gui = DetectorGUI()
detector_gui.root.withdraw()

# data table window
data_window = ShowDataGUI()
data_window._root.withdraw()

# detector gui window will be showed
# after successful login
login_gui.set_next(detector_gui)

# attaching data window to data button
detector_gui.set_data(data_window)

# back action will show detector
data_window.set_back(detector_gui)

root.mainloop()