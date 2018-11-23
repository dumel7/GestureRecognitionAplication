import queue
import torch
from PyQt5.QtCore import QThread
from torchvision.transforms import Compose, CenterCrop, ToTensor, Normalize
from PIL import Image
from model import MyNetwork
import numpy as np
import multiprocessing as mp

class PytorchModel(QThread):

    def __init__(self, chartSignal, parent=None):
        QThread.__init__(self, parent)
        self.chartSignal = chartSignal
        self.open_flag = False
        self.model = MyNetwork(5)
        self.transform = Compose([
            CenterCrop(84),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406],
                      std=[0.229, 0.224, 0.225])
        ])
        #frame, rgb, width, height
        self.images = torch.empty(1, 3, 84, 84)

    def __del__(self):
        self.wait()

    def open_model(self, path, details):
        self.path = path
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['state_dict'])
        details.setText(self.model.__str__())
        self.model.eval()
        self.open_flag = True

    def add_to_queue(self, q_image):
        if self.open_flag:
            bytes = q_image.bits().asstring(q_image.byteCount())
            pil_img = Image.frombuffer("RGB", (q_image.width(), q_image.height()), bytes, 'raw', "RGB", 0, 1)
            tensor_img = self.transform(pil_img)
            if self.images.shape[0] == 18:
                self.eval_model()
                self.get()
            self.append(tensor_img)

    def get(self):
        self.images = self.images.narrow(0, 0, 17)

    def append(self, tensor_img):
        tensor_img = tensor_img.view(1, 3, 84, 84)
        self.images = torch.cat((tensor_img, self.images), 0)

    def eval_model(self):
        test_val = self.images.view(1,3,18,84,84)
        output = self.model(test_val)
        output = output.detach().numpy()
        self.chartSignal.emit(output[0])







