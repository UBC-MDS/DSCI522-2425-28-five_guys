import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_and_engineer_data import clean_and_engineer_data

@pytest.fixture
def raw_data():
    return pd.DataFrame({
        'Date': ['2024-01-01', '2024-02-01'],
        'Temperature(°C)': [10, 20],
        'Humidity(%)': [70, 80],
        'Rainfall(mm)': [0, 5],
        'Snowfall (cm)': [0, 0],
        'Wind speed (m/s)': [3.5, 5.0],
        'Visibility (10m)': [10, 12],
        'Solar Radiation (MJ/m2)': [2.5, 3.0],
        'Dew point temperature(°C)': [5, 10],
        'Seasons': ['Spring', 'Winter'],
        'Holiday': ['Holiday', 'No Holiday'],
        'Functioning Day': ['Yes', 'No']
    })

def test_clean_and_engineer_data(raw_data):
    processed_data = clean_and_engineer_data(raw_data)
    assert 'Year' in processed_data.columns
    assert 'Month' in processed_data.columns
    assert 'Day' in processed_data.columns
    assert processed_data['Holiday'].isin([0, 1]).all()
