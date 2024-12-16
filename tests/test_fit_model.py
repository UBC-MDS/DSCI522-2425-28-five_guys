# tests/test_fit_model.py
import pytest
import os
import pickle
from pathlib import Path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.fit_model import fit_model

# Temporary directories for saving models
TEMP_PIPELINE_DIR = "results/models/temp/"
os.makedirs(TEMP_PIPELINE_DIR, exist_ok=True)

# Test data paths
TEMP_TRAINING_DATA = "data/processed/bike_train.csv"
PREPROCESSOR_PATH = "results/models/bike_preprocessor.pickle"


@pytest.fixture(scope="module")
def setup_and_teardown():
    """Fixture to clean up the pipeline files after the tests"""
    yield
    if os.path.exists(TEMP_PIPELINE_DIR):
        for file in os.listdir(TEMP_PIPELINE_DIR):
            os.remove(os.path.join(TEMP_PIPELINE_DIR, file))
        os.rmdir(TEMP_PIPELINE_DIR)

def test_fit_model_creates_ridge_pipeline(setup_and_teardown):
    """
    Test that fit_model function creates and saves the ridge pipeline pickle file.
    """
    try:
        # Run the model fitting function
        fit_model(TEMP_TRAINING_DATA, PREPROCESSOR_PATH, TEMP_PIPELINE_DIR, seed=522)
        
        # Check if the ridge pipeline pickle file is created
        ridge_pipeline_path = Path(TEMP_PIPELINE_DIR) / "ridge_pipeline.pickle"
        assert ridge_pipeline_path.is_file(), f"Ridge pipeline file was not created at {ridge_pipeline_path}"
    
    except Exception as e:
        pytest.fail(f"An error occurred while testing the ridge pipeline: {e}")

def test_fit_model_creates_tree_pipeline(setup_and_teardown):
    """
    Test that fit_model function creates and saves the decision tree pipeline pickle file.
    """
    try:
        # Run the model fitting function
        fit_model(TEMP_TRAINING_DATA, PREPROCESSOR_PATH, TEMP_PIPELINE_DIR, seed=522)
        
        # Check if the decision tree pipeline pickle file is created
        tree_pipeline_path = Path(TEMP_PIPELINE_DIR) / "tree_pipeline.pickle"
        assert tree_pipeline_path.is_file(), f"Decision tree pipeline file was not created at {tree_pipeline_path}"

    except Exception as e:
        pytest.fail(f"An error occurred while testing the decision tree pipeline: {e}")

def test_ridge_pipeline_not_empty(setup_and_teardown):
    """
    Test that the saved ridge pipeline pickle file is not empty.
    """
    try:
        # Check if the ridge pipeline pickle file exists and is not empty
        ridge_pipeline_path = Path(TEMP_PIPELINE_DIR) / "ridge_pipeline.pickle"
        with open(ridge_pipeline_path, 'rb') as f:
            ridge_pipeline = pickle.load(f)
            assert ridge_pipeline is not None, "Ridge pipeline is empty"
    
    except Exception as e:
        pytest.fail(f"An error occurred while checking the ridge pipeline: {e}")

def test_tree_pipeline_not_empty(setup_and_teardown):
    """
    Test that the saved decision tree pipeline pickle file is not empty.
    """
    try:
        # Check if the decision tree pipeline pickle file exists and is not empty
        tree_pipeline_path = Path(TEMP_PIPELINE_DIR) / "tree_pipeline.pickle"
        with open(tree_pipeline_path, 'rb') as f:
            tree_pipeline = pickle.load(f)
            assert tree_pipeline is not None, "Decision tree pipeline is empty"
    
    except Exception as e:
        pytest.fail(f"An error occurred while checking the decision tree pipeline: {e}")