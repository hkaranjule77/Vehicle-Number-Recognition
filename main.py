# third party packages
import tkinter as tk

# local packages
from NPR.gui.detector import DetectorGUI
from NPR.gui.login import Login
from NPR.ml_assets.plate_predictor import PlateRecognizer

# root window
root = tk.Tk()

# second window
detector_gui = DetectorGUI(tk.Toplevel())
detector_gui.root.withdraw()        # hides window

# first window
# login window drawn on root window
# next window will be of Detector window
login_gui = Login(root, next_window=detector_gui)

root.mainloop()
exit(0)