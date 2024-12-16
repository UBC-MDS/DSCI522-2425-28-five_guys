import pytest
import os
import numpy as np
import pandas as pd
import pandera as pa
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_validation import data_validation

# Test data setup
valid_data = pd.DataFrame({
    "Date":["1/4/2017", "5/6/2017", "8/3/2017"],
    "Rented Bike Count":[45, 235, 98],
    "Hour":[12, 5, 23],
    "Temperature(°C)": [10, 35, 16],
    "Humidity(%)":[12, 34, 23],
    "Wind speed (m/s)": [2.6, 1.4, 3.4],
    "Visibility (10m)": [100, 551, 565],
    "Dew point temperature(°C)": [-2, 5, 6],
    "Solar Radiation (MJ/m2)": [0.01, 0.05, 0.23],
    "Rainfall(mm)":[15.1, 5.0, 10.4],
    "Snowfall (cm)":[2.1, 0.4, 3.2],
    "Seasons":["Spring", "Summer", "Spring"],
    "Holiday":["Holiday", "No Holiday", "Holiday"],
    "Functioning Day":["Yes", "No", "No"]})

# Case: wrong type passed to function
valid_data_as_np = valid_data.copy().to_numpy()
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

# Case: columns with value restriction with values past upper bound
case_out_of_upper = valid_data.copy()
case_out_of_upper["Hour"] = case_out_of_upper["Hour"]+100
case_out_of_upper["Humidity(%)"] = case_out_of_upper["Humidity(%)"]+100 
invalid_data_case.append((case_out_of_upper, "Check numeric column values that are too large"))

# Case: columns with value restriction with values past lower bound
case_out_of_lower = valid_data.copy()
case_out_of_lower["Hour"] = case_out_of_lower["Hour"]-100
case_out_of_lower["Humidity(%)"] = case_out_of_lower["Humidity(%)"]-100
case_out_of_lower["Rented Bike Count"] = case_out_of_lower["Rented Bike Count"]-100
invalid_data_case.append((case_out_of_lower, "Check numeric column values that are too small"))

# Case: value in categorical columns not withint specified type
case_invalid_type = valid_data.copy()
case_invalid_type["Seasons"] = "Fall"
case_invalid_type["Holiday"] = "Yes"
case_invalid_type["Functioning Day"] = "Nope"
invalid_data_case.append((case_invalid_type, "Check invalid type for categorical columns"))

# Case: numerical columns with incorrect data type
case_invalid_data = valid_data.copy()
case_invalid_data["Temperature(°C)"] = case_invalid_data["Temperature(°C)"].fillna(0.0).astype(int)
case_invalid_data["Wind speed (m/s)"] = case_invalid_data["Wind speed (m/s)"].fillna(0.0).astype(int)
case_invalid_data["Dew point temperature(°C)"] = case_invalid_data["Dew point temperature(°C)"].fillna(0.0).astype(int)
case_invalid_data["Solar Radiation (MJ/m2)"] = case_invalid_data["Solar Radiation (MJ/m2)"].fillna(0.0).astype(int)
case_invalid_data["Rainfall(mm)"] = case_invalid_data["Rainfall(mm)"].fillna(0.0).astype(int)
case_invalid_data["Snowfall (cm)"] = case_invalid_data["Snowfall (cm)"].fillna(0.0).astype(int)
invalid_data_case.append((case_invalid_data, "Check invalid data type for numerical columns"))

# Case: duplicated rows
case_duplicate = valid_data.copy()
case_duplicate = pd.concat([case_duplicate, case_duplicate.iloc[[0], :]], ignore_index=True)
invalid_data_case.append((case_duplicate, f"Check absent or incorrect for duplicate rows"))

# Case: Empty rows present
case_missing_obs = valid_data.copy()
nan_row = pd.DataFrame([[np.nan] * (case_missing_obs.shape[1] - 1) + [np.nan]], columns=case_missing_obs.columns)
case_missing_obs = pd.concat([case_missing_obs, nan_row], ignore_index=True)
invalid_data_case.append((case_missing_obs, f"Check absent or incorrect for missing observations (e.g., a row of all missing values)"))

# Parameterize invalid data test cases
@pytest.mark.parametrize("invalid_data, description", invalid_data_case)
def test_valid_w_invalid_data(invalid_data, description):
    with pytest.raises(pa.errors.SchemaErrors) as exc_info:
        data_validation(invalid_data)