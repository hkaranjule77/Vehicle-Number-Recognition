from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *

import cv2
import threading
import numpy as np
import os
import time
from PIL import Image

from label_predictor import PlateRecognizer, Predictor

cam = None
count = 0
cam_thread = None

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
            cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
            cv2.putText(img,"Scan Saved",(15,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)

        return img, imgRoi
    return img, None


def cam_read():
    global cam
    count = 0

    cam_init()
    while cam.isOpened():
        success , img  = cam.read()

        if success:
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            img, _ = detect_plate(img, imgGray)
            cv2.imshow("Result",img)
            count += 1

        if cv2.waitKey(500) & 0xFF == ord('q'):
                cam.release()
                break


def cam_multi_thread():
    global cam_thread
    cam_thread = threading.Thread(target=cam_read)
    cam_thread.start()


def detect():
    success , img  = cam.read()
    if success:
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img, imgRoi = detect_plate(img, imgGray)

        if imgRoi is not None:
            print("Image write.")

            img_path = os.path.join('.', 'images',str(count)+".jpg")
            cv2.imwrite(img_path, imgRoi)

            pil_img = Image.fromarray(imgRoi)

            MODEL_PATH = os.path.join('..', 'train', 'harshad', 'text_recognition-ver-24.0.pth')

            predictor = Predictor(MODEL_PATH)
            print(predictor.predict(pil_img))

            #cv2.imshow("Roi",imgRoi)
            
        else:
            raise ValueError('No Number Plate Detected')
    else:
        raise ValueError('Camera cannot be opened.')

def cam_off():
    global cam_thread
    global cam
    if cam_thread:
        cam.release()
        cv2.destroyWindow("Result")
        cam_thread.join()
        cam_thread = None
    else:
        print("Camera is already off.")
    

if __name__ == '__main__':
    root = Tk()
    root.title("Vehicle Number Detection")
    root.geometry("480x480+650+50")
    root.configure(bg='light blue')

    btnopenCam = Button(root, text="CAMERA ON", width=20, font=('arial',18,'bold'), command=cam_multi_thread)
    btnDetect = Button(root, text="DETECT", width=20, font=('arial',18,'bold'), command=detect)
    ent_number = Entry(root, bd=5, font=('arial',18,'bold'))
    btnConfirm = Button(root, text="CONFIRM", width=20, font=('arial',18,'bold'))
    btnDetect = Button(root, text="DETECT", width=20, font=('arial',18,'bold'), command=detect)
    btn_close_cam = Button(root, text="CAMERA OFF", width=20, font=('arial',18,'bold'), command=cam_off)

    btnDetect.pack(pady=20)
    ent_number.pack(pady=20)
    btnConfirm.pack(pady=20)
    btnopenCam.pack(pady=20)
    btn_close_cam.pack(pady=20)

    root.mainloop()

