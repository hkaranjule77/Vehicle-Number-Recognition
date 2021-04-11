import requests
import json
import os
import threading    

dir_name = 'indian-car-dataset'

try:
    os.mkdir(dir_name)
except FileExistsError:
    pass

def download_img(url):
    ''' Downloads dataset using provided json file.'''
    sub_urls = url.strip().split('/')
    img_file_name = sub_urls[len(sub_urls) - 1]

    if os.path.exists(os.path.join(dir_name, img_file_name )):
        print(dir_name +'/' + img_file_name, 'already exist.')
        return
    
    file_req = requests.get(url, allow_redirects = True)

    img_path = os.join(dir_name, img_file_name)
    img_file = open(img_path, "wb+")
    img_file.write( file_req.content )
    img_file.close()

    print(dir_name +'/' + img_file_name, ' downloaded.')


count = 0

for json_line in open("./Indian_Number_plates.json", 'r'):
    # print(json_line)
    img_data_dict = json.loads(json_line)
    url = img_data_dict['content']

    thread = threading.Thread(target=download_img(url))
    thread.start()

    count += 1
    
print('Total files in india-car-dataset: ', count, end=' ')