"""
This file contains used constants
"""

START_DATE = "2021-01-01"  # Дата начала, формат YYYY-MM-DD
END_DATE = "2021-06-03"
# Общий список тиктов на выгрузку
SECURITY_LIST = ["AFLT","YNDX", "ALRS", "SBER", "MOEX"]
DATA_PATH = "app/loaded_data/"  # Путь к директории для выгрузки
PREDICTION_PATH = "app/predict_data/"
LAZY_PREDICTION_PATH = "app/lazy_predict_data/"
INTERVAL = 1  # Интервал, 1 = 1 мин, 10 = 10 мин, 60 = 1 час, 24 = 1 день
