import os

ROOT_DIR = os.getcwd()  # repo folder

# SRC
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
NPR_DIR = os.path.join(ROOT_DIR, 'NPR')

# ROOT DIR
DB_FILE = os.path.join(NPR_DIR, 'db.py')
GUI_DIR = os.path.join(NPR_DIR, 'gui')
ML_ASSETS_DIR = os.path.join(NPR_DIR, 'ml_assets')


# GUI
DETECTOR_GUI = os.path.join(GUI_DIR, 'detector.py')
LOGIN_GUI = os.path.join(GUI_DIR, 'login.py')
GUI_IMAGES = os.path.join(GUI_DIR, 'images')

# ML_COMPONENTS
PLATE_CASCADE = os.path.join(ML_ASSETS_DIR, 'haarcascade_russian_plate_number.xml')
PLATE_PREDICTOR = os.path.join(ML_ASSETS_DIR, 'plate_predictor.py')