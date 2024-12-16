import pytest
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.dummy import DummyRegressor
from src.model_evaluation import (
    load_data,
    load_pipeline,
    evaluate_model,
    save_results,
    generate_prediction_plot,
)


@pytest.fixture
def setup_test_environment(tmp_path):
    # Create mock test data
    test_data = pd.DataFrame(
        {
            "Temperature": [15, 20, 25],
            "Humidity": [50, 55, 60],
            "Wind speed": [5, 7, 9],
            "Rented Bike Count": [150, 200, 250],
        }
    )
    test_data_path = tmp_path / "test_data.csv"
    test_data.to_csv(test_data_path, index=False)

    # Create mock models
    ridge_model = DummyRegressor(strategy="mean")
    ridge_model.fit(test_data.drop("Rented Bike Count", axis=1), test_data["Rented Bike Count"])

    tree_model = DummyRegressor(strategy="constant", constant=200)
    tree_model.fit(test_data.drop("Rented Bike Count", axis=1), test_data["Rented Bike Count"])

    # Save models as pickle files
    ridge_model_path = tmp_path / "ridge_model.pkl"
    tree_model_path = tmp_path / "tree_model.pkl"

    with open(ridge_model_path, "wb") as f:
        pickle.dump(ridge_model, f)

    with open(tree_model_path, "wb") as f:
        pickle.dump(tree_model, f)

    return test_data_path, ridge_model_path, tree_model_path, tmp_path


def test_load_data(setup_test_environment):
    test_data_path, _, _, _ = setup_test_environment
    data = load_data(str(test_data_path))
    assert not data.empty, "Data should load correctly"
    assert "Rented Bike Count" in data.columns, "Target column should exist"


def test_load_pipeline(setup_test_environment):
    _, ridge_model_path, _, _ = setup_test_environment
    model = load_pipeline(str(ridge_model_path))
    assert model is not None, "Pipeline should load successfully"


def test_evaluate_model(setup_test_environment):
    test_data_path, ridge_model_path, _, _ = setup_test_environment
    model = load_pipeline(str(ridge_model_path))
    data = load_data(str(test_data_path))
    X_test = data.drop("Rented Bike Count", axis=1)
    y_test = data["Rented Bike Count"]
    score = evaluate_model(model, X_test, y_test)
    assert score == pytest.approx(0.0, rel=0.1), "Model evaluation score should be correct"


def test_save_results(setup_test_environment):
    _, _, _, tmp_path = setup_test_environment
    output_file = tmp_path / "results.csv"
    save_results(0.9, 0.85, str(output_file))
    assert os.path.isfile(output_file), "Results file should be created"
    results = pd.read_csv(output_file)
    assert "accuracy_ridge" in results.columns, "accuracy_ridge column should exist"
    assert "accuracy_tree" in results.columns, "accuracy_tree column should exist"


def test_generate_prediction_plot(setup_test_environment):
    test_data_path, ridge_model_path, _, tmp_path = setup_test_environment
    model = load_pipeline(str(ridge_model_path))
    data = load_data(str(test_data_path))
    X_test = data.drop("Rented Bike Count", axis=1)
    y_test = data["Rented Bike Count"]
    output_file = tmp_path / "plot.png"
    generate_prediction_plot(model, X_test, y_test, str(output_file))
    assert os.path.isfile(output_file), "Prediction plot should be created"