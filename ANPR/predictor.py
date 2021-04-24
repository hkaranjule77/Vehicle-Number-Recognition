import albumentations
import numpy as np
import os

import torch
from torch._C import dtype
import torch.nn as nn
import torch.nn.functional as F



from sklearn import preprocessing

DEVICE = 'cpu'
IMAGE_HEIGHT = 50
IMAGE_WIDTH = 230
NUM_WORKERS = 0

class Predictor:
    def __init__(self, model_path):
        if torch.cuda.is_available():
            DEVICE = 'cuda'
        else:
            DEVICE = 'cpu'
        checkpoint = torch.load(
                            model_path,
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
        ''' Takes raw prediction of models and decodes it into label '''
        predictions = predictions.permute(1, 0, 2)
        predictions = torch.softmax(predictions, 2)
        predictions = torch.argmax(predictions, 2)
        predictions = predictions.detach().cpu().numpy()

        preds = []
        for prediction in predictions:
            temp = ''
            prev_char = None
            for k in prediction:
                k = k - 1
                if k == -1 or prev_char == k:
                    prev_char = None
                    continue
                else:
                    temp += self.encoder.inverse_transform([k])[0]
                prev_char = k
            preds.append(temp)
        return temp
            

    def predict(self, pil_img):
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
        pred, _ = self.model(data)
        pred = self.decode_predictions(pred)
        return pred



# model

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

    ROOT_DIR = '..'
    MODELS_DIR = os.path.join(ROOT_DIR, 'train')
    TRAINER_DIR = os.path.join(MODELS_DIR, 'harshad')
    MODEL_FILE = 'text_recognition-ver-18.0.pth'
    MODEL_PATH = os.path.join(TRAINER_DIR, MODEL_FILE)

    img_path = '/home/hkaranjule77/Desktop/project/sem6-mini/Vehicle-Detection/datasets/gen-plate-dataset/AP 00AX 6535.png'
    pil_img = Image.open(img_path)

    predictor = Predictor(MODEL_PATH)
    print(predictor.predict(pil_img=pil_img))
