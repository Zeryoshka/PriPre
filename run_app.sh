#!/bin/bash

python3.9 -m venv env
source env/bin/activate
pip install -r requirements.txt
python run.py
