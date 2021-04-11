# indian-car-dataset to plate-dataset

import cv2
import os
import json

CAR_DATASET = 'indian-car-dataset'
PLATE_DATASET_PATH = 'plate-dataset'

def log_error(error_type, data):
    with open('not_found.log', 'a+') as not_found_file:
            not_found_file.write(error_type + ': ' + data + '\n')


file_index = 433

name_log_file = open('indian-car-dataset-to_plate_dataset.csv', 'w+')
name_log_file.write('Car_img_name, Plate_img_name;\n')

for json_line in open('Indian_Number_plates.json'):
    car_data = json.loads(json_line)
    file_url = car_data['content']
    file_url = file_url.split('/')
    file_name = file_url[len(file_url) - 1]

    # print(car_data['annotation'])

    #car img parameters
    img_height = car_data["annotation"][0]['imageHeight']
    img_width = car_data["annotation"][0]['imageWidth']

    # plate position ratios
    x_min = int(img_width * car_data["annotation"][0]['points'][0]['x'])
    y_min = int(img_height * car_data["annotation"][0]['points'][0]['y'])    
    x_max = int(img_width * car_data["annotation"][0]['points'][1]['x'])
    y_max = int(img_height * car_data["annotation"][0]['points'][1]['y'])

    try:
        img_path = os.path.join(CAR_DATASET, file_name)
        car_img = cv2.imread( img_path )
        plate_img = car_img[y_min: y_max, x_min: x_max]>
        # cv2.imshow('plate', plate_img)
        
        new_file_name = 'plate' + str(file_index) + '.jpeg'
        plate_img_path = os.path.join(PLATE_DATASET_PATH, new_file_name)
        cv2.imwrite(plate_img_path, plate_img)
    except FileNotFoundError:
        log_error('FileNotFoundError in car_img', file_name)

    name_log_file.write(file_name + ', ' + new_file_name + ';\n')
    file_index += 1

    #print(file_name, img_height, img_width, x_min, y_min, x_max, y_max)
