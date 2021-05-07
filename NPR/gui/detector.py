# third-party package
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

import cv2
import os
import sys
import threading
import time

# local package absolute imports
import filepaths as fp
from NPR.ml_assets.plate_predictor import PlateRecognizer, Predictor
from NPR.db import insert_plate



class Camera:
    ''' Class for Camera activation, reading. '''
    def __init__(self):
        self.cam = None
        self.count = 0
        self.cam_thread = None
        self.frameWidth = 640                   #Frame Width
        self.franeHeight = 480                  # Frame Height
        self.__detect_mode = False


    def __read(self):
        ''' Starts reading images from camera after '''
        if not self.isCanvasSet():
            raise ValueError('Canvas for image display is not set.')
        prev = time.time()
        while self.cam.isOpened():
            if not self.__detect_mode:
                success , img  = self.cam.read()
                elapsed_time = time.time()
                if success and (elapsed_time - prev > 0.3):
                    try:
                        prev = elapsed_time
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img_tk = ImageTk.PhotoImage(Image.fromarray(img))
                        self.img_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
                    except AttributeError:
                        pass
                    except RuntimeError:
                        pass
                    except tk.TclError:
                        pass
            


    def getDetectFrame(self):
        ''' When Detect Mode is on, returs 
        a newly read frame(color, gray) from VideoCapture object. '''
        if self.__detect_mode:
            success, frame = self.cam.read()
            color_frame = cv2.cvtColor(frame, 
                        cv2.COLOR_BGR2RGB)
            gray_frame = cv2.cvtColor(frame, 
                        cv2.COLOR_BGR2GRAY)
            if success:
                return (color_frame, gray_frame)
            else:
                raise cv2.CameraError(
                    'Cannot read a frame from camera. ')
        else:
            raise Camera.CameraError(
                'Please turn on Detet Mode is mode first.')


    def isCanvasSet(self):
        ''' Checks if canvas is intitialized. 
        If yes then returns true else false. '''
        if self.img_canvas == None:
            return False
        return True


    def isReading(self):
        '''Checks if camera is on returns true 
        else if it's off then returns false. '''
        if self.cam is None:
            return False
        elif self.cam.isOpened():
            return True
        else:
            return False


    def setCanvas(self, canvas):
        ''' Initialize canvas for displaying images. '''
        if type(canvas)==tk.Canvas:
            self.img_canvas = canvas
            # print('Hello canvas has been set successfully')
        else:
            raise TypeError('canvas should be of type \''+type(tk.Canvas)+'\'')

    def setDetectOn(self):
        ''' This mode stops video rendering on GUI 
        and activates getFrame method. '''
        self.__detect_mode = True

    def setDetectOff(self):
        ''' Moves out of Detect Mode and 
        starts rendering video on predefined cavas.'''
        self.__detect_mode = False

    def turnOff(self):
        '''
        Switches off the camera recording 
        if camera is on and returns true on success.
        Else if raises CameraError
        '''
        if self.cam is not None and self.cam.isOpened():
            self.cam.release()
        else:
            raise Camera.TurnOffError('Camera cannot be closed properly.')


    def turnOn(self):
        '''
        Creates new thread for camera and 
        starts reading images from it to form a video.
        '''
        if self.cam is None or not self.cam.isOpened():
            self.cam = cv2.VideoCapture(0)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.frameWidth)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.franeHeight)
            self.cam.set(cv2.CAP_PROP_SATURATION, 150)

            cam_thread = threading.Thread(target=self.__read)
            cam_thread.start()
            # print("Is camera thread alive?", cam_thread.is_alive())
        else:
            raise Camera.TurnOnError('Camera cannot be turned on')


    class CameraError(Exception):
        pass

    class TurnOnError(Exception):
        pass

    class TurnOffError(Exception):
        pass



class PlateDetector:
    ''' Methods for Number Plate detection and Recognition '''
    def __init__(self):
        # camera parameters
        self.detect_state = False               # used for detect action
        self.plateCascade = cv2.CascadeClassifier(fp.PLATE_CASCADE)
        self.predictor = Predictor()


    def detect_number(self, imgROI):
        ''' Initialize PlateRecognizer model and 
        predicts the labels for passed plate image. '''
        pil_img = Image.fromarray(imgROI)
        prediction = self.predictor.predict(pil_img)
        return prediction


    def detect_plate(self, img, imgGray):
        ''' Detects Plate from passed img(color, gray) image.'''
        minArea = 500
        numberPlates = self.plateCascade.detectMultiScale(
                            imgGray, 1.1, 4)

        for (x, y, w, h) in numberPlates:
            area = w*h
            if area > minArea:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, "NumberPlate", (x,y-5), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                imgRoi = img[y:y+h, x:x+w]
                return img, imgRoi
        return img, None
    
class CorrectionGUI:
    ''' Correction window class for Vehicle Registration Number. '''
    def __init__(self, plate_label):
        # GUI configuration
        self._root = tk.Toplevel()
        self._root.title('VRN Correction')
        self._root.geometry('500x160+700+100')
        self._root.config(bg='light blue')
        # GUI elements
        self.lbl_plate = tk.Label(self._root, 
                text="Enter correct Vehicle Registration Number:", 
                font=("times new roman", 15), bg="light blue")
        self.txt_plate = tk.Entry(self._root, font=("times new roman", 15), 
                bg="lightgray")
        self.txt_plate.insert(0, plate_label)
        self.btn_confirm = tk.Button(self._root, text="Confirm", 
                font=("times new roman", 15), command=self.confirm)
        # placing
        self.lbl_plate.place(x=25, y=10)
        self.txt_plate.place(x=25, y=50)
        self.btn_confirm.place(x=25, y=100)

    def confirm(self):
        ''' Method for Confirm button and saves data. '''
        self._root.withdraw()
        if insert_plate(self.txt_plate.get()):
            messagebox.showinfo(title='Data saved',
                message="Veicle Registration Number data saved successfully.")
        else:
            messagebox.showerror(title='Data not saved',
                message="Error in saving Vehicle Registration Number.")
        


class DetectorGUI:
    ''' GUI made for Detection using tkinter third-party library. '''
    DATA_WINDOW = 1

    def __init__(self, data_window=None):
        # GUI COMPONENTS
        self.root = tk.Toplevel()
        self.root.title("Vehicle Number Detection")
        self.root.config(bg="light blue")
        self.root.geometry("1040x530+50+50")
        self.root.protocol("WM_DELETE_WINDOW", self.progExit)
        # video(continous images) but for now a still image is added
        self.img_canvas = tk.Canvas(self.root, width=640, height=480)
        img_path = os.path.join(fp.GUI_IMAGES, 'bg1.jpg')
        # print(img_path)
        logo_upb = ImageTk.PhotoImage(file=img_path)
        self.root.logo_upb = logo_upb       # to prevent getting collected in garbage
        self.img_canvas.create_image(0, 0, anchor=tk.NW, image=logo_upb)
        self.detector = PlateDetector()
        # camera
        self.cam = None
        self.plate_label = None
        self.next_window = None
        self.__data_window = data_window

        # buttons
        self.label_info = tk.Label(self.root, text="Click CAMERA ON", 
            width=15, bd=5, font=('arial',18,'bold'))
        self.btnopenCam = tk.Button(self.root, text="CAMERA ON", 
            width=15, font=('arial',18,'bold'),command=self.camOn)
        self.btn_close_cam = tk.Button(self.root, text="CAMERA OFF", 
            width=15, font=('arial',18,'bold'), command=self.camOff)
        self.btnDetect = tk.Button(self.root, text="DETECT", 
            width=15, font=('arial',18,'bold'), command=self.detectPlateNumber)
        self.btn_data = tk.Button(self.root, text="DATA", 
            width=15, font=('arial',18,'bold'), command=self.show_data)
        self.btn_close_win = tk.Button(self.root, text="EXIT", 
            width=15, font=('arial',18,'bold'), command=self.progExit)

        # components placing
        self.img_canvas.grid(row=0, column=0, rowspan=7, columnspan=1, padx=(25, 25), pady=(25, 25))
        self.label_info.grid(row=0, column=1, columnspan=1, padx=(5, 25), pady=(25, 5))
        self.btnopenCam.grid(row=1, column=1, columnspan=1, padx=(5, 25), pady=(5, 5))
        self.btn_close_cam.grid(row=2, column=1, columnspan=1, padx=(5, 25), pady=(5, 5))
        self.btnDetect.grid(row=3, column=1, columnspan=1, padx=(5, 25), pady=(5, 5))
        self.btn_data.grid(row=4, column=1, columnspan=1, padx=(5, 25), pady=(5, 5))
        self.btn_close_win.grid(row=5, column=1, columnspan=1, padx=(5, 25), pady=(5, 25))


    def camOff(self):
        ''' Switches off the camera and hence the video component. '''
        if self.cam is not None:
            self.cam.turnOff()
            self.label_info['text'] = 'Camera status:\nOFF'
            self.cam = None
        else:
            messagebox.showinfo(message="Camera is already off")


    def camOn(self):
        ''' Initializes camera, sets canvas for video component 
        and turns it on. '''
        if self.cam is None:
            self.cam = Camera()
            try:
                self.cam.setCanvas(self.img_canvas)
                self.cam.turnOn()
                self.label_info['text'] = 'Camera status:\nON'
            except Camera.TurnOnError:
                messagebox.showerror(title="Error in Camera",
                    message="Camera cannot be turned on.\nError Code: 1")
        elif self.cam.isReading():
            messagebox.showinfo(title="Camrea is already ON.", 
                    message="Please turn off camera when not required.")
        else:
            messagebox.showerror(title="Error in Camera",
                    message="Camera cannot be turned on.\nError Code: 2")


    def clear_next_window(self):
        ''' Clears next_window attribute of Detector GUI. '''
        self.next_window = None

    def deiconify(self):
        ''' Redraws detector window. '''
        self.root.deiconify()


    def detectPlateNumber(self):
        ''' Method to be called by the click action of detect button. '''
        if self.cam is not None:
            self.btnDetect['state'] = 'disable'
            self.cam.setDetectOn()
            detect_thread = threading.Thread(target=self.detectThread)
            detect_thread.start()
        else:
            messagebox.showerror(title="Camera is off", 
                        message="Please click \"CAMERA ON\" button first.")


    def detectThread(self):
        ''' Method for detection to be executed on new Thread. ''' 
        color_frame, gray_frame = self.cam.getDetectFrame()
        plate_img, imgROI = self.detector.detect_plate(color_frame, gray_frame)
        if imgROI is not None:
            tk_plate_img = ImageTk.PhotoImage(Image.fromarray(plate_img))
            time.sleep(0.5)
            self.img_canvas.create_image(0, 0, anchor=tk.NW, image=tk_plate_img)
            plate_label = self.detector.detect_number(imgROI)
            DetectorGUI.save_plate(plate_label)            
        else:
            messagebox.showinfo(title="Plate Detection", 
                message="No plate found in image.")
        self.btnDetect['state'] = 'normal'
        self.cam.setDetectOff()


    def progExit(self):
        ''' Turns camera off and exits the execution. '''
        if self.cam is not None and self.cam.isReading():
            try:
                self.cam.turnOff()
            except Camera.TurnOffError:
                messagebox.showerror(title="Camera Error",
                    message="Camera not closed properly.")
        self.root.withdraw()
        exit(0)


    def save_plate(plate_label):
        ''' Method for confirmation and saving Vehicle Registraion Number. '''
        is_correct = messagebox.askyesno(title="Confirm Plate Number",
                            message="Is this '"+plate_label+"' right?")
        if is_correct == True:
            if insert_plate(plate_label):
                messagebox.showinfo(title='Data saved',
                    message="Veicle Registration Number data saved successfully.")
            else:
                messagebox.showerror(title='Data not saved',
                    message="Error in saving Vehicle Registration Number.")
        else:
            correction = CorrectionGUI(plate_label)


    def set_data(self, data_window=None):
        ''' Set window instance for Data button. '''
        self.__data_window = data_window


    def show_data(self):
        ''' Set next_window parameter to DATA_WINDOW. '''
        try:
            self.cam.turnOff()
        except Camera.CameraError:
            pass
        except AttributeError:
            pass
        self.root.withdraw()
        self.__data_window.deiconify()