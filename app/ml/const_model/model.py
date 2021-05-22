import json
from random import randint

class Const:
    '''
    Test class for describing model
    '''
    def __init__(self):
        '''
        Init method for Const class
        '''
        self.weight = None

    def load(self):
        '''
        Function for loading weights/parametrs from file
        '''
        with open('param.json', 'r') as f:
            self.weight = json.load(f)['weight']

    def predict(self, x_old, y_old, x_pred):
        '''
        Main method which using for predict model CONST
        '''
        y_pred = []
        for x in x_pred:
            y_pred.append(self.weight)
        return y_pred

    def fit(self):
        '''
        Function for learning model (not use in production, but use for preparing)
        '''
        self.weight = randint(0, 1000)

    def dump(self):
        '''
        Method for save weight in file after fit
        '''
        with open('param.json', 'w') as f:
            json.dump({'weight': self.weight}, f)