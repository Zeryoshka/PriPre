from .config import FILE_LOAD_MODEL
from .config import FILE_LOAD_K
from .config import FILE_DUMP_MODEL
from .config import FILE_DUMP_K
from .config import FEATURES_COUNT
from .config import EPHOS_FIT

from .utils import reshaper
from .utils import normalise
from .utils import predict_reshaper

import json
import tensorflow as tf
from tensorflow import keras
import pandas as pd

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
        self.model = keras.models.load_model(
            FILE_LOAD_MODEL
        )

    def dump(self):
        """
        Method for save weight in file after fit
        """
        with open(FILE_DUMP_K, 'w') as f:
            json.dump({
                'k': self.k
            }, f)
        self.model.save(FILE_DUMP_MODEL, save_format='h5')

    def predict(self, base_prices, time_axis):
        """
        Main method used for predict model It is alive
        """
        x_closes = predict_reshaper(base_prices, FEATURES_COUNT) / self.k
        out_data = pd.DataFrame(columns=['begin', 'close'])
        for time_str in time_axis:
            model_in = pd.DataFrame(x_closes).transpose()
            val = self.model.predict(model_in)[0][0]
            out_data = out_data.append({
                'begin': time_str,
                'close': val
            }, ignore_index=True)
  
            x_closes = x_closes.shift(1)
            x_closes['close1'] = val
        out_data['close'] = out_data['close'] * self.k

        return out_data

    def lazy_predict(self, test):
        '''
        Main method used for fast predict, without generation
        of line in model It is alive
        '''
        new_test = reshaper(test, FEATURES_COUNT)
        new_test['close'] = self.model.predict(
            normalise(
                new_test[
                    [f'close{i}' for i in range(1,FEATURES_COUNT+1)]
                ],
                FEATURES_COUNT, 
                self.k
            )
        ) * self.k

        return new_test[['begin', 'close']]

    def fit(self, train, verbose=2):
        """
        Function for learning model
        (not use in production, but use for preparing)
        """
        self.k = max(abs(train['close'].max()), abs(train['close'].min()))
        train_norm = normalise(
            reshaper(train, FEATURES_COUNT), FEATURES_COUNT, self.k
        )
        self.model.fit(
            train_norm[[f'close{i}' for i in range(1, FEATURES_COUNT + 1)]],
            train_norm['close'],
            epochs=EPHOS_FIT,
            verbose=verbose
        )

    def compile_model(self):
        """
        Compile model function
        (Use for compile model in case somebody break it)
        """
        self.model = keras.Sequential([
            keras.layers.Flatten(input_shape=(FEATURES_COUNT,)),
            keras.layers.Dense(64, activation=tf.nn.silu),
            keras.layers.Dense(26, activation=tf.nn.softplus),
            keras.layers.Dense(24, activation=tf.nn.silu),
            keras.layers.Dense(40, activation=tf.nn.silu),
            keras.layers.Dense(30, activation=tf.nn.relu),
            keras.layers.Dense(30, activation=tf.nn.softplus),
            keras.layers.Dense(30, activation=tf.nn.relu),
            keras.layers.Dense(64, activation=tf.nn.silu),
            keras.layers.Dense(1, activation=tf.nn.relu),
        ])
        self.model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001, rho=0.9),
            loss='mse', 
            metrics=['mse', 'mae']
        )