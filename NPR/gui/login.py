# third party package
from PIL import Image, ImageTk
from tkinter import *
from tkinter import messagebox

import os

# local package
import filepaths as fp


class Login:
    ''' Login GUI made with tkinter '''

    def __init__(self, root, next_window=None):
        self.root = root
        self.root.title("LOGIN SYSTEM")
        self.root.geometry("1000x600+50+50")
        img_path = os.path.join(fp.GUI_IMAGES, 'bg.jpg')
        self.bg = ImageTk.PhotoImage(file=img_path)
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=150, y=150, height=340, width=500)

        title = Label(Frame_login, text="LOGIN HERE", font=("impact", 35, "bold"), fg="#d77337",
                      bg="white").place(x=90, y=30)
        desc = Label(Frame_login, text="NUMBER PLATE DATA", font=("Goudy old style", 15, "bold"), fg="#d25d17",
                     bg="white").place(x=90, y=100)

        lbl_user = Label(Frame_login, text="USERNAME", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=90, y=140)
        self.txt_user = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
        self.txt_user.place(x=90, y=170, width=350, height=35)

        lbl_pass = Label(Frame_login, text="PASSWORD", font=("Goudy old style", 15, "bold"), fg="gray",
                         bg="white").place(x=90, y=210)
        self.txt_pass = Entry(Frame_login, show="*", font=("times new roman", 15), bg="lightgray")
        self.txt_pass.place(x=90, y=240, width=350, height=35)

        Login_btn = Button(self.root, command=self.login_function, cursor="hand2", text="LOGIN", fg="white",
                           bg="#d77337", font=("times new roman", 20)).place(x=300, y=470, width=180, height=40)
        self.next_window = next_window

    def login_function(self):
        '''
        This fuction is executed when login button is pressed.
        1) Validate credentials 
        2) If credentials are right then moves to next window 
        '''
        if self.txt_pass.get() == "" or self.txt_user.get() == "":
            messagebox.showerror("ERROR", "ALL FIELDS ARE REQUIRED", parent=self.root)
        elif self.txt_pass.get() != "1234" or self.txt_user.get() != "test":
            messagebox.showerror("ERROR", "INVALID USERNAME/PASSWORD", parent=self.root)
        else:
            self.root.withdraw()
            if self.next_window is not None:
                self.next_window.root.deiconify()
            else:
                exit(0)


if __name__ == '__main__':
    # -------FIRST LOGIN PAGE--------
    root = Tk()
    obj = Login(root)

    root.mainloop()
