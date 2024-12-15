import pytest
import os
import numpy as np
import pandas as pd
import pandera as pa
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_validation import data_validation

# Test data setup
# valid_data = pd.DataFrame({
#     "Date":["1/4/2017", "5/6/2017", "8/3/2017"],
#     "Rented Bike Count":[45, 235, 98],
#     "Hour":[12, 5, 23]
#     "Temperature(°C)": [10, 35, 16],
#     "Humidity(%)":[12, 34, 23],
#     "Wind speed (m/s)": [2.6, 1.4, 3.4],
#     "Visibility (10m)": [100, 551, 565],
#     "Dew point temperature(°C)": [-2, 5, 6],
#     "Solar Radiation (MJ/m2)": [0.01, 0.05, 0.23],
#     "Rainfall(mm)":[15.1, 5.0, 10.4],
#     "Snowfall (cm)":[2.1, 0.4, 3.2],
#     "Seasons":["Spring", "Summer", "Spring"],
#     "Holiday":["Holiday", "No Holiday", "Holiday"],
#     "Functioning Day":["Yes", "No", "No"]})

# Case: wrong type passed to function
valid_data_as_np = valid_data.copy().to_nump()
def test_valid_data_type():
    with pytest.raises(TypeError):
        data_validation(valid_data_as_np)

# Case: empty data frame
case_empty_data_frame = valid_data.copy().iloc[0:0]
def test_valid_data_empty_data_frame():
    with pytest.raises(ValueError):
        data_validation(case_empty_data_frame)

# Setup list of invalid data cases
invalid_data_case=[]

# Case: missing "Rented Bike Count" column
case_missing_column = valid_data.copy()
case_missing_column = case_missing_column.drop("Rented Bike Count", axis=1) 
invalid_data_case.append((case_missing_column, "check missing `Rented Bike Count` column from DataFrame schema"))

# Case: value in "Hour" column too large
case_outside_hour_bound = valid_data.copy()
case_outside_hour_bound["Hour"] = case_outside_hour_bound["Hour"]+10 
invalid_data_case.append((case_outside_hour_bound, "Check numeric value in `Hour` column that are too large"))

# Case: value in "Seasons" is not type

# Case: duplicated rows

# Case: Empty rows present