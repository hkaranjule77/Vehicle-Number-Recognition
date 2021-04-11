from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import cv2
import numpy as np

def f1():
	

    frameWidth = 640    #Frame Width
    franeHeight = 480   # Frame Height

    plateCascade = cv2.CascadeClassifier("E:\ML\ANPR\haarcascade_russian_plate_number.xml")
    minArea = 500

    cap =cv2.VideoCapture(0)
    cap.set(3,frameWidth)
    cap.set(4,franeHeight)
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


root = Tk()
root.title("Vehicle Number Detection")
root.geometry("480x480+650+50")
root.configure(bg='light blue')

btnopenCam = Button(root, text="cam", width=20, font=('arial',18,'bold'), command=f1 )
btnDetect = Button(root, text="DETECT", width=20, font=('arial',18,'bold'))
ent_number = Entry(root, bd=5, font=('arial',18,'bold'))
btnConfirm = Button(root, text="CONFIRM", width=20, font=('arial',18,'bold'))

btnDetect.pack(pady=20)
ent_number.pack(pady=20)
btnConfirm.pack(pady=20)
btnopenCam.pack(pady=20)

root.mainloop()

