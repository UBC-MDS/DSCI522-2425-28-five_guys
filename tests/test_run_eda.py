# tests/test_run_eda.py
import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.run_eda import run_eda
from pathlib import Path
# four tests created to check eda 1. format check for png files 2. format check for csv files 3. check sizes of png files 4. check sizes of csv files 
# List of expected test PNG plot filenames 
EXPECTED_PNG_FILES = [
    "test_rented_bike_count.png",
    "test_hourly_rental_count.png",
    "test_season_rental_count.png",
    "test_season_temp_count.png",
    "test_holiday_dist.png",
    "test_season_hourly.png",
    "test_corr_chart.png"
]

# List of expected test CSV table filenames
EXPECTED_CSV_FILES = [
    "test_missing_values.csv",
    "test_summary_stats.csv"
]


temp_plot_directory = "results/figures"
temp_table_directory = "results/tables"
processed_dataframe = "data/processed/bike_train.csv"



def test_run_eda_creates_png_files():
    """
    Test that run_eda generates all expected PNG files in the plot directory.
    """
    try:
        # Run the EDA script
        run_eda(processed_dataframe, temp_plot_directory, temp_table_directory)
        
        # Check for missing PNG files
        missing_png_files = [
            file for file in EXPECTED_PNG_FILES
            if not (Path(temp_plot_directory) / file).is_file()
        ]
    except FileNotFoundError as e:
        print(f"FileNotFoundError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while checking PNG files: {e}")


def test_run_eda_creates_csv_files():
    """
    Test that run_eda generates all expected CSV files in the table directory.
    """
    try:
        # Run the EDA script
        run_eda(processed_dataframe, temp_plot_directory, temp_table_directory)
        
        # Check for missing CSV files
        missing_csv_files = [
            file for file in EXPECTED_CSV_FILES
            if not (Path(temp_table_directory) / file).is_file()
        ]
    except FileNotFoundError as e:
        print(f"FileNotFoundError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while checking CSV files: {e}")



def test_non_empty_csv_files():
    """
    Test that run_eda generates all expected CSV files and ensures none of them are empty (size = 0).
    """
    try:
        # Run the EDA script
        print('Running EDA script...')
        run_eda(processed_dataframe, temp_plot_directory, temp_table_directory)
        
        # Check that all CSV files have a size greater than 0
        non_zero_size_csv_files = [
            file for file in EXPECTED_CSV_FILES
            if os.path.getsize(Path(temp_table_directory) / file) == 0  # Check if file size is greater than 0
        ]
        
        if non_zero_size_csv_files:
            raise ValueError(f"The following CSV files are not empty (size == 0 bytes): {non_zero_size_csv_files}")
        
    except FileNotFoundError as e:
        print(f"FileNotFoundError occurred: {e}")
        raise
    except ValueError as e:
        print(f"ValueError occurred: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while checking for non-empty CSV files: {e}")
        raise  # re-raise the exception so the test fails

def test_empty_png_files():
    """
    Test that run_eda generates all expected PNG files and ensures none of them are 0 in size.
    """
    try:
        # Run the EDA script
        run_eda(processed_dataframe, temp_plot_directory, temp_table_directory)
        
        # Check for zero-size PNG files
        zero_size_png_files = [
            file for file in EXPECTED_PNG_FILES
            if os.path.getsize(Path(temp_plot_directory) / file) == 0
        ]
        if zero_size_png_files :
            raise ValueError(f"The following PNG files are not empty (size == 0 bytes): {zero_size_png_files}")

    except FileNotFoundError as e:
        print(f"FileNotFoundError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while checking for empty PNG files: {e}")

