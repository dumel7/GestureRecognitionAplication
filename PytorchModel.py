import torch

from model import MyNetwork


class PytorchModel:

    def __init__(self, path):
        self.path = path
        self.model = MyNetwork(5)
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['state_dict'])

    def get_model_details(self):
        return self.model.__str__()

