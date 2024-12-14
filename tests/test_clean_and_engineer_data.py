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

def test_column_renaming(raw_data):
    processed_data = clean_and_engineer_data(raw_data)
    expected_columns = ['Temperature', 'Humidity', 'Rainfall', 'Snowfall', 'Wind speed',
                        'Visibility', 'Radiation', 'Dew point temperature', 'Year', 
                        'Month', 'Day', 'Weekday', 'Seasons', 'Holiday', 'Functioning Day']
    assert all(col in processed_data.columns for col in expected_columns), "Column renaming failed."

def test_date_conversion(raw_data):
    processed_data = clean_and_engineer_data(raw_data)
    assert processed_data['Year'].iloc[0] == 2024
    assert processed_data['Month'].iloc[0] == 1
    assert processed_data['Day'].iloc[0] == 1
    assert processed_data['Weekday'].iloc[0] == 0, "Incorrect weekday for 2024-01-01"

def test_binary_encoding(raw_data):
    processed_data = clean_and_engineer_data(raw_data)
    assert processed_data['Holiday'].iloc[0] == 1, "Holiday binary encoding failed."
    assert processed_data['Holiday'].iloc[1] == 0, "Holiday binary encoding failed."
    assert processed_data['Functioning Day'].iloc[0] == 1, "Functioning Day binary encoding failed."
    assert processed_data['Functioning Day'].iloc[1] == 0, "Functioning Day binary encoding failed."

