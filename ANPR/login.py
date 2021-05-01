from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np
import threading
import time

from label_predictor import PlateRecognizer, Predictor
from db import insert_plate


class Login:
	def __init__(self,root):
		self.root=root
		self.root.title("LOGIN SYSTEM")
		self.root.geometry("1000x600+650+50")
		img_path = os.path.join('.', 'GUI-imgs', 'bg.jpg')
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
		self.txt_pass=Entry(Frame_login, show="*", font=("times new roman",15),bg="lightgray")
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

cam = None
count = 0
cam_thread = None
detect_state = False
label_info = None

CASCADE_PATH = os.path.join('.', 'haarcascade_russian_plate_number.xml')

def cam_init():
    frameWidth = 640    #Frame Width
    franeHeight = 480   # Frame Height
    global cam
    cam = cv2.VideoCapture(0)
    cam.set(3,frameWidth)
    cam.set(4,franeHeight)
    cam.set(10,150)

    global plateCascade
    plateCascade = cv2.CascadeClassifier(CASCADE_PATH)



def detect_plate(img, imgGray):
    minArea = 500
    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,"NumberPlate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            imgRoi = img[y:y+h,x:x+w]
            #cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
            #cv2.putText(img,"Scan Saved",(15,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)

            return img, imgRoi
    return img, None


def cam_read():
    global cam
    global logo_upb
    global img_canvas
    global detect_state
    count = 0
    imgRoi = None

    cam_init()
    while cam.isOpened():
        success , img  = cam.read()

        if success:
            if detect_state:
                imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img, imgRoi = detect_plate(img, imgGray)

            try:
                img_for_gui = Image.fromarray(img)
                logo_upb =ImageTk.PhotoImage(img_for_gui)
                img_canvas.create_image(0, 0, anchor=NW, image=logo_upb)
                # cv2.imshow("Result",img)
                count += 1
            except:
                pass

            if detect_state:
                detect_state = False
                if imgRoi is not None:
                    time.sleep(8)
                    imgRoi = None

"""         if cv2.waitKey(500) & 0xFF == ord('q'):
            cam.release() """


def cam_multi_thread():
    global cam_thread, cam, label_info
    if cam is None:
        cam_thread = threading.Thread(target=cam_read)
        cam_thread.start()
        label_info['text'] = "Camera status: \nON"
    else:
        messagebox.showerror(title="Camrea is already on.", message="Please turn off camera when not required.")


def detect_number():
    global label_info
    if cam is not None:
        success , img  = cam.read()
        if success:
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, imgRoi = detect_plate(img, imgGray)

            if imgRoi is not None:
                #cv2.imshow("Roi",imgRoi)
                MODEL_PATH = os.path.join('..', 'train', 'harshad', 'text_recognition-ver-24.0.pth')
                predictor = Predictor(MODEL_PATH)
                pil_img = Image.fromarray(imgRoi)
                prediction = predictor.predict(pil_img)
                # label_info['text'] = "Number plate: " + prediction

                correct_pred = messagebox.askyesno(title="Vehicle Number Plate Confirmation",
                                    message="\n"+prediction+"'\n\nIs this correct?")

                if correct_pred:
                    if insert_plate(prediction):
                        messagebox.showinfo(title="Record saved", 
                            message=prediction+" record added succesfully.")
            else:
                #raise ValueError('No Number Plate Detected')
                messagebox.showerror(message="No Number Plate Detected.")


def detect_on():
    global detect_state
    if cam is not None:
        if detect_state:
            return
        else:
            detect_state = True
            detect_number()
    else:
        messagebox.showerror(title="Camera is off", 
                    message="Please click \"CAMERA ON\" button first.")


def cam_off():
    global cam_thread
    global cam
    global label_info
    if cam_thread:
        cam.release()
        time.sleep(2)
        cam = None
        label_info['text'] = 'Camera status:\n OFF'
    else:
        #print("Camera is already off.")
        messagebox.showinfo(message="Camera is already off")


def prog_exit():
    ''' Program exit '''
    global vehicle
    global cam_thread
    global cam

    if cam is not None:
        cam.release()
    vehicle.withdraw()
    exit(0)


#-------FIRST LOGIN PAGE--------
root=Tk()
obj=Login(root)


#-------CAMERA-----------------
vehicle = Toplevel(root)
vehicle.title("Vehicle Number Detection")
vehicle.geometry("1020x510+650+50")
vehicle.config(bg="light blue")

img_canvas = Canvas(vehicle, bg="white", width=620, height=460)

img_path = os.path.join('.', 'GUI-imgs', 'bg1.jpg')
logo_upb =ImageTk.PhotoImage(file=img_path)

img_canvas.create_image(0, 0, anchor=NW, image=logo_upb)


btnopenCam = Button(vehicle, text="CAMERA ON", width=15, font=('arial',18,'bold'),command=cam_multi_thread)
btnDetect = Button(vehicle, text="DETECT", width=15, font=('arial',18,'bold'), command=detect_on)
label_info = Label(vehicle, text="Click CAMERA ON", width=15, bd=5, font=('arial',18,'bold'))
#btnConfirm = Button(vehicle, text="CONFIRM", width=15, font=('arial',18,'bold'))
btn_close_cam = Button(vehicle, text="CAMERA OFF", width=15, font=('arial',18,'bold'), command=cam_off)
btn_close_win = Button(vehicle, text="EXIT", width=15, font=('arial',18,'bold'), command=prog_exit)

img_canvas.grid(row=0, column=0, rowspan=6, columnspan=1, padx=(25, 25), pady=(25, 25))
label_info.grid(row=0, column=1, columnspan=1, padx=(5, 25), pady=(25, 5))
#btnConfirm.grid(row=2, column=2, columnspan=1, padx=(5, 25), pady=(5, 5))
btnopenCam.grid(row=1, column=1, columnspan=1, padx=(5, 25), pady=(5, 5))
btn_close_cam.grid(row=2, column=1, columnspan=1, padx=(5, 25), pady=(5, 5))
btnDetect.grid(row=3, column=1, columnspan=1, padx=(5, 25), pady=(5, 5))
btn_close_win.grid(row=4, column=1, columnspan=1, padx=(5, 25), pady=(5, 25))
vehicle.withdraw()

root.mainloop()

exit(0)