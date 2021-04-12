# referred: https://mlblr.com/includes/dataset/index.html

from PIL import ImageFont, ImageDraw, Image  
import numpy as np 
import cv2
import os
import random

# ASCII A to Z are 65 to 90

hel = [75, 25, 15, 130, 120] 
beb = [110, 2, 60, 135, 150]


#use a truetype font 
#font = ImageFont.truetype("Helvetica-Bold.ttf", 120)  
font = ImageFont.truetype("BebasNeueBold.ttf", 45)  

PLATE_DIR = 'gen-plate-dataset'

try:
    os.mkdir(PLATE_DIR)
except FileExistsError:
    pass


rtc = 67
bias = 10
for r in range(rtc+1):
    if r < 4:
        for k in range(500):
            if r < 10:
                number_plate_1 = "MH 0" + str(r)
            else:
                number_plate_1 = "MH " + str(r)
            number_plate_1 += (chr(random.randint(65, 90))+chr(random.randint(65, 90))+" " + str(random.randint(1000, 9999)))
            img = np.zeros((50, 230, 3), np.uint8)
            pil_img = Image.fromarray(img)
            draw = ImageDraw.Draw(pil_img)

            draw.text((16, 7), number_plate_1, font=font)  
            #draw.text((15, 130), number_plate_2, font=font)
            cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            cv2_img = cv2.bitwise_not(cv2_img)

            #cv2.imshow("number_plate", cv2_img)
            img_path = os.path.join(PLATE_DIR, number_plate_1+".png")
            cv2.imwrite(img_path, cv2_img)
            #cv2.waitKey(10)
    else:
        for k in range(100):
            if r < 10:
                number_plate_1 = "MH 0" + str(r)
            else:
                number_plate_1 = "MH " + str(r)
            number_plate_1 += (chr(random.randint(65, 90))+chr(random.randint(65, 90))+" " + str(random.randint(1000, 9999)))
            img = np.zeros((50, 230, 3), np.uint8)
            pil_img = Image.fromarray(img)
            draw = ImageDraw.Draw(pil_img)

            draw.text((16, 8), number_plate_1, font=font)  
            # draw.text((15, 130), number_plate_2, font=font)
            cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            cv2_img = cv2.bitwise_not(cv2_img)

            #cv2.imshow("number_plate", cv2_img)
            img_path = os.path.join(PLATE_DIR, number_plate_1+".png")
            cv2.imwrite(img_path, cv2_img)
            #cv2.waitKey(10)



#cv2.destroyAllWindows()
