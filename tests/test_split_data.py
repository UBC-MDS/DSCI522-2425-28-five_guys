import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_data import split_data

@pytest.fixture
def raw_data():
    return pd.DataFrame({
        'Temperature': [10, 20],
        'Humidity': [70, 80],
        'Rainfall': [0, 5]
    })

def test_split_data(raw_data):
    train, test = split_data(raw_data)
    assert len(train) + len(test) == len(raw_data)
