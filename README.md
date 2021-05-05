# Vehicle Number Detection

This project will detect Vehicle Registration Number(VRN) with help of **OpenCV** and **PyTorch** library of **Python**.


### Directory Structure

Vehicle-Number-Recognition(repository)
|
|---NPR(Number Plate Recognition Package)
|   |---gui
|   |   |---images
|   ----ml_assets
|---datasets
|---notebooks
----models

# How to run this project?

> git clone 

### How to install third-party libraries?(production)

We recommend to use a `conda/virtualenv environment` before installing third-party libraries for this project.
> conda create -n environment_name python==3.8
> conda activate environment_name

and change directory to cloned repository excute following command to install required libraries:
> pip install -r requirements.txt

# References
- OpenCV docs: https://docs.opencv.org/master/d6/d00/tutorial_py_root.html
- PyTorch docs: https://pytorch.org/docs/stable/index.html
- Haar features: https://www.youtube.com/watch?v=F5rysk51txQ
- RCNN Architecture: https://www.youtube.com/watch?v=IcLEJB2pY2Y&t=3161s
