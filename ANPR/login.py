from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np

img_path = os.path.join('.', 'GUI-imgs', 'bg1.jpg')

class Login:
	def __init__(self,root):
		self.root=root
		self.root.title("LOGIN SYSTEM")
		self.root.geometry("1000x600+100+50")
		self.bg=ImageTk.PhotoImage(file=img_path)
		self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)

		Frame_login=Frame(self.root,bg="white")
		Frame_login.place(x=150,y=150,height=340,width=500)

		title=Label(Frame_login,text="LOGIN HERE",font=("impact",35,"bold"),fg="#d77337",bg="white").place(x=90,y=30)
		desc=Label(Frame_login,text="NUMBER PLATE DATA",font=("Goudy old style",15,"bold"),fg="#d25d17",bg="white").place(x=90,y=100)
		
		lbl_user=Label(Frame_login,text="USERNAME",font=("Goudy old style",15,"bold"),fg="gray",bg="white").place(x=90,y=140)
		self.txt_user=Entry(Frame_login,font=("times new roman",15),bg="lightgray")
		self.txt_user.place(x=90,y=170,width=350,height=35)

		lbl_pass=Label(Frame_login,text="PASSWORD",font=("Goudy old style",15,"bold"),fg="gray",bg="white").place(x=90,y=210)
		self.txt_pass=Entry(Frame_login,font=("times new roman",15),bg="lightgray")
		self.txt_pass.place(x=90,y=240,width=350,height=35)
	
		Login_btn=Button(self.root,command=self.login_function,cursor="hand2",text="LOGIN",fg="white",bg="#d77337",font=("times new roman",20)).place(x=300,y=470,width=180,height=40)
		
	def login_function(self):
		if self.txt_pass.get()=="" or self.txt_user.get()=="":
			messagebox.showerror("ERROR","ALL FIELDS ARE REQUIRED",parent=self.root)
		elif self.txt_pass.get()!="1234" or self.txt_user.get()!="test":
			messagebox.showerror("ERROR","INVALID USERNAME/PASSWORD",parent=self.root)
		else:
			root.withdraw()
			vehicle.deiconify()

def f1():
	

    frameWidth = 640    #Frame Width
    frameHeight = 480   # Frame Height

    plateCascade = cv2.CascadeClassifier("E:\ML\ANPR\haarcascade_russian_plate_number.xml")
    minArea = 500

    cap =cv2.VideoCapture(0)
    cap.set(3,frameWidth)
    cap.set(4,frameHeight)
    cap.set(10,150)
    count = 0

    while True:
        success , img  = cap.read()

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        numberPlates = plateCascade .detectMultiScale(imgGray, 1.1, 4)

        for (x, y, w, h) in numberPlates:
            area = w*h
            if area > minArea:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img,"NumberPlate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                imgRoi = img[y:y+h,x:x+w]
                cv2.imshow("ROI",imgRoi)
        cv2.imshow("Result",img)
        if cv2.waitKey(1) & 0xFF ==ord('s'):
            cv2.imwrite("E:\ML\Vehicle-Registration-Detection\ANPR\images\img"+str(count)+".jpg",imgRoi)
            cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
            cv2.putText(img,"Scan Saved",(15,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
            cv2.imshow("Result",img)
            
            cv2.waitKey(500)
            count+=1

def f2():
	login.withdraw()
	vehicle.deiconify()


#-------FIRST LOGIN PAGE--------
root=Tk()
obj=Login(root)


#-------CAMERA-----------------
vehicle = Toplevel(root)
vehicle.title("Vehicle Number Detection")
vehicle.geometry("1020x510+650+50")
vehicle.configure(bg='light blue')

img_canvas = Canvas(vehicle, width=620, height=460)

img_path = os.path.join('.', 'GUI-imgs', 'bg1.jpg')
print(os.path.exists(img_path))
logo_upb =ImageTk.PhotoImage(file=img_path)
'''
label = Label(vehicle, image=logo_upb,height=480,width=640)
label.image = logo_upb
label.place(bordermode=INSIDE, x=0, y=0)
'''

img_canvas.create_image(0, 0, anchor=NW, image=logo_upb)


btnopenCam = Button(vehicle, text="cam", width=15, font=('arial',18,'bold'),command=f1 )
btnDetect = Button(vehicle, text="DETECT", width=15, font=('arial',18,'bold'))
ent_number = Entry(vehicle, bd=5, font=('arial',18,'bold'))
btnConfirm = Button(vehicle, text="CONFIRM", width=15, font=('arial',18,'bold'))

img_canvas.grid(row=0, column=0, rowspan=4, columnspan=1, padx=(25, 25), pady=(25, 25))
btnDetect.grid(row=0, column=2, columnspan=1, padx=(5, 25), pady=(25, 5))
ent_number.grid(row=1, column=2, columnspan=1, padx=(5, 25), pady=(5, 5))
btnConfirm.grid(row=2, column=2, columnspan=1, padx=(5, 25), pady=(5, 5))
btnopenCam.grid(row=3, column=2, columnspan=1, padx=(5, 25), pady=(5, 25))
#label.grid(row=0,column=0)


""" img_canvas.pack(side=LEFT)
btnDetect.pack(side=BOTTOM)
ent_number.pack(side=BOTTOM)
btnConfirm.pack(side=BOTTOM)
btnopenCam.pack(side=BOTTOM) """
#label.grid(row=0,column=0)

vehicle.withdraw()


root.mainloop()