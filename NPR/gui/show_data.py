import tkinter as tk
from tkinter import font

# local package absoulte import
from NPR.db import select_plate



class ShowDataGUI:
    ''' Shows all recorded VRN data from DB. '''
    def __init__(self, back_window=None):
        self._root = tk.Toplevel()
        self.LABEL_BG = "light blue"
        self._root.geometry('660x520+100+100')
        self._root.config(bg='light blue')
        self._root.protocol("WM_DELETE_WINDOW", exit)
        self.add_components()
        self.__back_window = back_window

    def add_components(self):
        ''' fetchs data and arranges components on the screen. '''
        data = select_plate()
        
        # table headers
        sr_no_lbl = tk.Label(self._root, text="Sr No", width=6,  
                font=('times new roman', 16, tk.font.BOLD),
                bg=self.LABEL_BG, borderwidth=2, relief="solid")
        datetime_lbl = tk.Label(self._root, text="Recored at", width=19,
                font=('times new roman', 16, tk.font.BOLD), 
                bg=self.LABEL_BG, borderwidth=2, relief="solid")
        vrn_label = tk.Label(self._root, text="Vehicle Number", width=14,
                font=('times new roman', 16, tk.font.BOLD), 
                bg=self.LABEL_BG, borderwidth=2, relief="solid")
        
        # header placing
        sr_no_lbl.grid(row=0, column=0, padx=(25,5), pady=(25, 5))
        datetime_lbl.grid(row=0, column=1, padx=(5, 5), pady=(25, 5))
        vrn_label.grid(row=0, column=2, padx=(5,25), pady=(25, 5))
        
        # data from database
        row_index = 0
        while row_index < len(data):
            date_time, vrn = data[row_index]
            date_time = date_time.strftime("%Y/%m/%d %H:%M:%S %p")
            # data labels
            sr_no_lbl = tk.Label(self._root, text=str(row_index+1), width=7, 
                    font=('times new roman', 16), bg=self.LABEL_BG,
                    borderwidth=2, relief="groove")
            date_time_lbl = tk.Label(self._root, text=date_time, width=25,
                    font=('times new roman', 16), bg=self.LABEL_BG,
                    borderwidth=2, relief="groove")
            number_lbl = tk.Label(self._root, text=vrn, width=18,
                    font=('times new roman', 16), bg=self.LABEL_BG,
                    borderwidth=2, relief="groove")
            # data label placing
            sr_no_lbl.grid(row=row_index+1, column=0, padx=(25, 5))
            date_time_lbl.grid(row=row_index+1, column=1, padx=(5, 5))
            number_lbl.grid(row=row_index+1, column=2, padx=(5, 25))
            row_index += 1

        self.btn_back = tk.Button(self._root, text="Back", font=("time new romam", 18),
                        command=self.go_back)
        self.btn_back.grid(row=row_index+1, column=2, padx=(25, 25), pady=(25, 25))

    def deiconify(self):
        ''' Redraws ShowData window. '''
        self._root.deiconify()

    def go_back(self):
        ''' Takes back to detector window. '''
        self._root.withdraw()
        if self.__back_window is not None:
            self.__back_window.deiconify()

    def set_back(self, back_window=None):
        ''' To set back action of Data Window. '''
        self.__back_window = back_window

            