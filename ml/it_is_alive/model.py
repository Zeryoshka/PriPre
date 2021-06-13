from numpy.core.fromnumeric import shape
from .config import FILE_LOAD_MODEL
from .config import FILE_LOAD_K
from .config import FILE_DUMP_MODEL
from .config import FILE_DUMP_K
from .config import FEATURES_COUNT
from .config import EPHOS_FIT

from .utils import reshaper
from .utils import normalise

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ["CUDA_VISIBLE_DEVICES"]= '-1' 

import json
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np


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

    def load(self, from_files=[FILE_LOAD_K, FILE_LOAD_MODEL]):
        """
        Function for loading weights/parametrs from file
        from_files - list with 2 file names
        (first - k-file, second - model-file)
        """
        with open(from_files[0], 'r') as f:
            self.k = json.load(f)['k']
        self.model = keras.models.load_model(
            from_files[1]
        )

    def dump(self, to_files=[FILE_DUMP_K, FILE_DUMP_MODEL]):
        """
        Method for save weight in file after fit
        to_files - list with 2 file names
        (first - k-file, second - model-file)
        """
        with open(to_files[0], 'w') as f:
            json.dump({
                'k': self.k
            }, f)
        self.model.save(to_files[1], save_format='h5')

    def predict(self, base_prices, time_axis):
        """ 
        Main method used for predict model It is alive
        
        base_prices - Series with one column, which len is more then FEATURES_COUNT
        it is more then FEATURES_COUNT last prices of current_ticket
        time_axis - Series with time-strings for prediction
        """
        x_closes = np.array(base_prices[-FEATURES_COUNT:]) / self.k
        out_data = pd.DataFrame(columns=['begin', 'close'])
        for time_str in time_axis:
            val = self.model.predict(x_closes.reshape((1, FEATURES_COUNT)))[0][0]
            out_data = out_data.append({
                'begin': time_str,
                'close': val
            }, ignore_index=True)
            x_closes = np.append([val], x_closes[:-1])
        out_data['close'] = out_data['close'] * self.k

        return out_data

    def lazy_predict(self, df):
        '''
        Main method used for fast predict, without generation
        of line in model It is alive
        df - DataFrame with ['close', 'begin'] len: FEATURES_COUNT(from train)+test
        '''
        new_test = reshaper(df, FEATURES_COUNT)
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

        train - DataFrame with to column ['close', 'begin'] for training
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
            keras.layers.Dense(128, activation=tf.nn.softplus),
            keras.layers.Dense(128, activation=tf.nn.silu),
            keras.layers.Dense(64, activation=tf.nn.softplus),
            keras.layers.Dense(32, activation=tf.nn.softplus),
            keras.layers.Dense(16, activation=tf.nn.silu),
            keras.layers.Dense(8, activation=tf.nn.softplus),
            keras.layers.Dense(4, activation=tf.nn.silu),
            keras.layers.Dense(1, activation=tf.nn.softplus),
        ])
        self.model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001, rho=0.9),
            loss='mse', 
            metrics=['mse', 'mae']
        )