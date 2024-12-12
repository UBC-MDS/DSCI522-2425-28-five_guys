
# split_n_preprocessing.py
# date: 2024-12-05

import os
import click
import pandas as pd
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean_and_engineer_data import clean_and_engineer_data
from src.split_data import split_data
from src.create_preprocessor import create_preprocessor
from src.save_object import save_object


@click.command()
@click.option('--raw_data', type=str, help="Path to raw data")
@click.option('--data_to', type=str, help="Path to directory where processed data will be written to")
@click.option('--preprocessor_to', type=str, help="Path to directory where the preprocessor object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)
def main(raw_data, data_to, preprocessor_to, seed):
    """
    This script reads in the cleaned up data, splits the data into train and test sets,
    preprocesses it for exploratory data analysis, and saves the preprocessor used in
    the model training script.
    """
    # Set the random seed for reproducibility
    df = pd.read_csv(raw_data, encoding="latin-1")

    # Step 1: Clean and engineer the data
    df = clean_and_engineer_data(df)

    # Step 2: Split the data into training and testing sets
    bike_train, bike_test = split_data(df, test_size=0.3, random_state=seed)

    # Save the train and test datasets
    os.makedirs(data_to, exist_ok=True)
    bike_train.to_csv(os.path.join(data_to, "bike_train.csv"), index=False)
    bike_test.to_csv(os.path.join(data_to, "bike_test.csv"), index=False)

    # Step 3: Create the preprocessor
    bike_preprocessor = create_preprocessor()

    # Save the preprocessor object
    os.makedirs(preprocessor_to, exist_ok=True)
    save_object(bike_preprocessor, os.path.join(preprocessor_to, "bike_preprocessor.pickle"))


if __name__ == '__main__':
    main()
