# Vehicle Number Recognition

This project will detect Vehicle Registration Number(VRN) with help of **OpenCV** and **PyTorch** library of **Python**.


### Repository Structure

Vehicle-Number-Recognition(repository)  
|  
|---NPR(Number Plate Recognition Package)  
|&nbsp;&nbsp;&nbsp;&nbsp;|---gui  
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|---images  
|&nbsp;&nbsp;&nbsp;&nbsp;|---ml_assets  
|---datasets  
|---notebooks  
|---models

# Software Requirements
- Python 3.x
- PIP (package manager for python)
##### For Linux:
```
sudo apt install python3
sudo apt install python3-pip
````
##### For Windows:
Installion guide for Python & PIP: https://docs.python.org/3/using/windows.html
  
# How to install?
Change your currend working directory of `terminal/CMD` to desired location to download VNR Repository and execute following command:
```
git clone https://github.com/hkaranjule77/Vehicle-Number-Recognition.git
```

### How to install third-party libraries?(production)

**(optional)** Before installing third-party library, we recommend to use a `conda/virtualenv environment`to create new environment to avoid dependecy conflict. Use following commands to create new environment: 
```
conda create -n environment_name python==3.8

conda activate environment_name
```  
Change current working directory into cloned repository and excute the following command in `terminal/CMD` to install required libraries:
```
pip install -r requirements.txt
```  
# How to run?
Linux:
```
python3 main.py
```
Windows:
```
python main.py
```
>**NOTE:** Don't forget to add python environment variable in your machine or it will throw external command error.

# References
- OpenCV docs: https://docs.opencv.org/master/d6/d00/tutorial_py_root.html
- PyTorch docs: https://pytorch.org/docs/stable/index.html
- Haar features: https://www.youtube.com/watch?v=F5rysk51txQ
- RCNN Architecture: https://www.youtube.com/watch?v=IcLEJB2pY2Y&t=3161s
