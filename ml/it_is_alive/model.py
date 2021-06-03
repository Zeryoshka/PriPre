from .config import FILE_LOAD_MODEL
from .config import FILE_LOAD_K
from .config import FILE_DUMP_MODEL
from .config import FILE_DUMP_K

from .utils import reshaper
from .utils import normalise

import json
import tensorflow as tf
from tensorflow import keras

class It_is_alive:
    """
    It is alive class for describing model
    """

    def __init__(self):
        """
        Init method for It_is_alive class
        """
        self.model = None
        self.k = None

    def load(self):
        """
        Function for loading weights/parametrs from file
        """
        with open(FILE_LOAD_K, 'r') as f:
            self.k = json.load(f)['k']
        self.model = keras.models.load_model(FILE_LOAD_MODEL)

    def dump(self):
        """
        Method for save weight in file after fit
        """
        with open(FILE_DUMP_K, 'w') as f:
            json.dump({
                'k': self.k
            }, f)
        self.model.save(FILE_DUMP_MODEL, save_format='h5')

    def predict(self, x_old, y_old, x_pred):
        """
        Main method which using for predict model CONST
        """
        y_pred = []
        for x in x_pred:
            y_pred.append(self.weight)
        return y_pred

    def fit(self, train_features, train_labels):
        """
        Function for learning model
        (not use in production, but use for preparing)
        """
        
        self.model.fit(
            train_norm[[f'close{i}' for i in range(1, FEATURES_COUNT + 1)]],
            train_norm['close'],
            epochs=10000,
            verbose=2
        )