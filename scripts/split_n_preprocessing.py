# split_n_preprocessing.py

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer

@click.command()
@click.option('--raw_data', type=str, help="Path to raw data")
@click.option('--data_to', type=str, help="Path to directory where processed data will be written to")
@click.option('--preprocessor_to', type=str, help="Path to directory where the preprocessor object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(raw_data, data_to, preprocessor_to, seed):
    '''
    This script reads in the cleaned up data and splits the data to train and test sets. The data gets
    preprocessed to be ready for exploratory data anaylsis and saves the preprocessor used in the model
    training script
    '''
    np.random.seed(seed)
    set_config(transform_output="pandas")
    df = pd.read_csv(raw_data)

    # renaming columns
    df = df.rename(columns={
    'Temperature(°C)': 'Temperature',
    'Humidity(%)': 'Humidity',
    'Rainfall(mm)': 'Rainfall',
    'Snowfall (cm)': 'Snowfall',
    'Wind speed (m/s)': 'Wind speed',
    'Visibility (10m)': 'Visibility',
    'Solar Radiation (MJ/m2)': 'Radiation',
    'Dew point temperature(°C)': 'Dew point temperature'})

    # Convert the Date column in Datetime Dtype
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')

    # Extract features from the Date column
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Weekday'] = df['Date'].dt.weekday
    df = df.drop(['Date'], axis=1)  # Exclude unwanted columns

    # Convert to categorical
    # df['Hour'] = df['Hour'].astype(str)
    df['Seasons'] = df['Seasons'].astype(str)

    # Converting to binary for EDA and for values to feed into model
    df['Holiday'] = df['Holiday'].apply(lambda x: 1 if x == "Holiday" else 0)
    df['Functioning Day'] = df['Functioning Day'].apply(
    lambda x: 1 if x == "Yes" else 0)

    # train-test split
    bike_train, bike_test = train_test_split(df, test_size=0.3, random_state=123)
    bike_train.to_csv(os.path.join(data_to, "bike_train.csv"), index=False)
    bike_test.to_csv(os.path.join(data_to, "bike_test.csv"), index=False)

    # Define column transformer for preprocessing
    bike_preprocessor = make_column_transformer(
        # One-hot encode Hour, Seasons, Year, Month and Day
        (OneHotEncoder(sparse_output=False), ['Hour', 'Seasons', 'Year', 'Month', 'Day']),
        ("drop", ['Dew point temperature']),
        remainder= StandardScaler()  # Leave other columns as they are
    )

    pickle.dump(bike_preprocessor, open(os.path.join(preprocessor_to, "bike_preprocessor.pickle"), "wb"))

    bike_preprocessor.fit(bike_train)
    scaled_bike_train = bike_preprocessor.transform(bike_train)
    scaled_bike_test = bike_preprocessor.transform(bike_test)

    scaled_bike_train.to_csv(os.path.join(data_to, "scaled_bike_train.csv"), index=False)
    scaled_bike_test.to_csv(os.path.join(data_to, "scaled_bike_test.csv"), index=False)


if __name__ == '__main__':
    main()