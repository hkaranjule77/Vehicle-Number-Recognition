import albumentations
import numpy as np
import os
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F

from sklearn import preprocessing

# local package
import filepaths as fp

IMAGE_HEIGHT = 50
IMAGE_WIDTH = 230
NUM_WORKERS = 0
MODEL_PATH = os.path.join(fp.MODELS_DIR, 'text_recognition-ver-30.0.pth')
if torch.cuda.is_available():
    DEVICE = 'cuda'
else:
    DEVICE = 'cpu'

class Predictor:
    '''
        Model Loader and Predictor for Number Plate Recognizer. 
        Use predict method which takes pil image as input and
           returns label for it.

        Example: 
        predictor = Predictor()
        
        img = Image.open(img_path)
        label = predictor.predict(img)
    '''
    def __init__(self):
        '''
            Initializor/Constructor for Predictor class. 
            Input: None
        '''
        checkpoint = torch.load(
                            MODEL_PATH,
                            map_location=torch.device(DEVICE)
                          )
        self.model = checkpoint['model']
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval() 
        self.aug = albumentations.Compose(
            [albumentations.Normalize(always_apply=True)]
        )

        classes = checkpoint['classes']
        self.encoder = preprocessing.LabelEncoder()
        self.encoder.fit(classes)

        

    def decode_predictions(self, predictions):
        ''' 
            Takes raw predictions of model and decodes it into one label.
            NOTE: It's many to one mapping for predictions to label.
            To make work it in production.
            It do two things:
            i) removes null charactor
            ii) removes repeated character

            Input:
                predictions: List of predictions
            Returns:
                label: String of processed single label
        '''
        predictions = predictions.permute(1, 0, 2)
        predictions = torch.softmax(predictions, 2)
        predictions = torch.argmax(predictions, 2)
        predictions = predictions.detach().cpu().numpy()
        wrapper = predictions

        preds = []
        for prediction in wrapper:
            label = ''
            prev_char = None
            for char in prediction:
                # 1 was added to include null character
                # subtracting 1 to remove it
                char = char - 1 
                # -1 is null character
                if char == -1 or prev_char == char:
                    prev_char = None
                    continue
                else:
                    label += self.encoder.inverse_transform([char])[0]
                prev_char = char

        # in production it predicts only img at a time
        # so, directly returning decoded string
        return label
            

    def predict(self, pil_img):
        ''' Predicts Number Plate by using passed PIL Image to get prediction.
            Input:
                pil_img: PIL Image of a Number Plate
            Returns:
                prediction: String of Number Plate Label 
         '''
        img = pil_img.resize(
                (IMAGE_WIDTH, IMAGE_HEIGHT),
                resample=Image.BILINEAR)
        img = np.array(img)
        augmented = self.aug(image=img)
        img = augmented['image']
        img_tensor = torch.tensor(img, dtype=torch.float)
        img_tensor = img_tensor.permute(2, 0, 1)
        img_tensor = img_tensor.unsqueeze(0)
        # print(img_tensor.shape)
        data = img_tensor.to(DEVICE)
        prediction, _ = self.model(data)
        prediction = self.decode_predictions(prediction)
        return prediction



# model class for plate recognition

class PlateRecognizer(nn.Module):
    def __init__(self, num_chars):
        super(PlateRecognizer, self).__init__()
        self.conv1 = nn.Conv2d(3,128, kernel_size=(3, 6), padding=(1, 1))
        self.max_pool_1 = nn.MaxPool2d(kernel_size=(2, 2))
        self.conv2 = nn.Conv2d(128, 64, kernel_size=(3, 6), padding=(1, 1))
        self.max_pool_2 = nn.MaxPool2d(kernel_size=(2, 2))

        self.linear = nn.Linear(768, 64)
        self.drop = nn.Dropout(0.2)  # doesn't change size

        self.gru = nn.GRU(64,
                          32,
                          bidirectional = True,
                          num_layers=2,
                          dropout=0.25,
                          batch_first=True
                         )
        self.output = nn.Linear(64, num_chars + 1)

    def forward(self, imgs, targets=None):
        bs, c, w, h = imgs.size()
        # print(bs, c, w, h)    # for debugging
        x = F.relu(self.conv1(imgs))
        # print('Conv1', x.size())
        x = self.max_pool_1(x)
        # print('MaxPool', x.size())
        x = F.relu(self.conv2(x))
        # print('Conv2', x.size())
        x = self.max_pool_2(x)  # 1, 64, 12, 57
        # print('MaxPool', x.size())

        # to brind width first but in our case it's properly arranged
        x = x.permute(0, 3, 1, 2)  # 1, 57, 64, 12
        # print('Permute', x.size())
        x = x.view(bs, x.size(1), -1)
        # print('View', x.size())

        x = self.linear(x)
        x = self.drop(x)
        # print('Linear', x.size())

        x, _ = self.gru(x)
        # print('Recurrent', x.size())

        x = self.output(x)
        # print('output', x.size())

        x = x.permute(1, 0, 2)
        '''
        # used for training
        if targets is not None:
            # CTC
            log_probs = F.log_softmax(x, 2)
            input_lengths = torch.full(size=(bs, ),
                                       fill_value=log_probs.size(0),
                                       dtype=torch.int32)
            # print('input lengths', input_lengths)
            target_lengths = torch.full(size=(bs, ),
                                        fill_value=targets.size(1),
                                        dtype=torch.int32)
            # print('target lengths', target_lengths)
            loss = nn.CTCLoss(blank=0)(log_probs, targets,
                                       input_lengths, target_lengths)
            return x, loss
        '''
        return x, None


if __name__ == '__main__':

    from PIL import Image

    img_path = '/home/hkaranjule77/Desktop/project/sem6-mini/Vehicle-Detection/datasets/gen-plate-dataset/AP 00AX 6535.png'
    pil_img = Image.open(img_path)

    predictor = Predictor()
    print(predictor.predict(pil_img=pil_img))
