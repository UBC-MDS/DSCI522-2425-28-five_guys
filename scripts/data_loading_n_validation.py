# data_pipeline.py
# date: 2024-12-05

import os
import zipfile
import io
import requests
import pandas as pd
import numpy as np
import pandera as pa
from deepchecks.tabular import Dataset
from deepchecks.checks import FeatureLabelCorrelation, FeatureFeatureCorrelation
from scipy.stats import skew
import click
import warnings

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=".*is_categorical_dtype is deprecated.*"
)


def read_zip(url, directory):
    # Tries to read in dataset from given url and save it in the data folder
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad status codes

    if not zipfile.is_zipfile(io.BytesIO(response.content)):
        raise ValueError("❌ The URL does not point to a valid ZIP file.")

    os.makedirs(directory, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        file_list = z.namelist()
        csv_files = [f for f in file_list if f.endswith(".csv")]

        if not csv_files:
            raise ValueError("❌ No CSV files found in the ZIP archive.")

        z.extractall(directory)
        print(f"Data validation 1-2 ✅ Extracted files and csv format ✅ : {file_list}")
        return os.path.join(directory, csv_files[0])


def validate_csv_schema(file_path):
    # Ensures that each column in the dataset adheres to the expected data type 
    # and satisfies the specified range and validation criteria.
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    except Exception as e:
        raise ValueError(f"❌ Error reading the CSV file: {e}")

    # Define Pandera schema
    schema = pa.DataFrameSchema(
        {
            "Date": pa.Column(str),
            "Rented Bike Count": pa.Column(int, pa.Check.between(0, np.inf)),
            "Hour": pa.Column(int, pa.Check.between(0, 23)),
            "Temperature(°C)": pa.Column(float),
            "Humidity(%)": pa.Column(int, pa.Check.between(0, 100)),
            "Wind speed (m/s)": pa.Column(float),
            "Visibility (10m)": pa.Column(int),
            "Dew point temperature(°C)": pa.Column(float),
            "Solar Radiation (MJ/m2)": pa.Column(float),
            "Rainfall(mm)": pa.Column(float,
                                      pa.Check(lambda s: s.isna().mean() <= 0.05, element_wise=False,
                                               error="Too many null values in 'Rainfall(mm)' column."),
                                      nullable=True),
            "Snowfall (cm)": pa.Column(float),
            "Seasons": pa.Column(str, pa.Check.isin(["Winter", "Summer", "Autumn", "Spring"])),
            "Holiday": pa.Column(str, pa.Check.isin(["Holiday", "No Holiday"])),
            "Functioning Day": pa.Column(str, pa.Check.isin(["Yes", "No"]))
        },
        checks=[
            pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
        ]
    )

    # Validate schema
    df = schema.validate(df, lazy=True).drop_duplicates().dropna(how="all")
    print("✅ CSV passed  data validation. 3-8")
    return df


def validate_additional_checks(df):
    # Check for skewness in the target variable
    target_column = "Rented Bike Count"
    if target_column in df.columns:
        if pd.api.types.is_numeric_dtype(df[target_column]):
            skewness_value = skew(df[target_column].dropna())
            print(f"Skewness of '{target_column}': {skewness_value:.2f}")
            if -1 <= skewness_value <= 1:
                raise ValueError(f"❌ The target variable '{target_column}' is not skewed.")
            else:
                print(f"✅ 9. The target variable '{target_column}' is skewed.")
        else:
            raise ValueError(f"❌ The target variable '{target_column}' is not numerical.")
    else:
        raise ValueError(f"❌ Column '{target_column}' does not exist in the DataFrame.")

    # Deepchecks: Feature-Label correlation
    deep_check = Dataset(df, label=target_column, cat_features=[])
    check_feat_lab_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.9)
    if not check_feat_lab_corr.run(dataset=deep_check).passed_conditions():
        raise ValueError("❌ Feature-Label correlation exceeds the maximum acceptable threshold.")
    else:
        print("✅ 10. No anomalous correlations between target/response variable and features.")

    # Deepchecks: Feature-Feature correlation
    check_feat_feat_corr = FeatureFeatureCorrelation()
    if not check_feat_feat_corr.run(dataset=deep_check).passed_conditions():
        raise ValueError("❌ Feature-Feature correlation issues detected.")
    else:
        print("✅ 11. No anomalous correlations between features.")
    return df


@click.command()
@click.option('--url', type=str, help="URL of the dataset to be downloaded.")
@click.option('--write_to', type=str, default="../data", help="Directory to save and validate raw data.")
def main(url, write_to):


    # Step 1: Download and extract ZIP file
    raw_data_dir = os.path.join(write_to)
    csv_path = read_zip(url, raw_data_dir)

    # Step 2: Validate CSV schema
    df = validate_csv_schema(csv_path)

    # Step 3: Perform additional data validation checks
    df = validate_additional_checks(df)


  

if __name__ == '__main__':
    main()
