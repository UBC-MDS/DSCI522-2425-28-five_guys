import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.metrics import PredictionErrorDisplay


def load_data(file_path: str):
    """
    Load the test data from a CSV file.

    Parameters:
    ----------
    file_path : str
        Path to the test data CSV file.

    Returns:
    -------
    pd.DataFrame 
        Loaded test data.
    """
    return pd.read_csv(file_path)


def load_pipeline(pipeline_path):
    """
    Load a machine learning pipeline object from a pickle file.

    Parameters:
    ----------
    pipeline_path : str 
        Path to the pipeline pickle file.

    Returns:
    -------
    object
        Loaded pipeline object.
    """
    with open(pipeline_path, "rb") as f:
        return pickle.load(f)


def evaluate_model(model, X, y):
    """
    Evaluate a model's performance on test data.

    Parameters:
    ----------
    model: sklearn model
        Trained model or pipeline.
    X : pd.DataFrame 
        Feature set.
    y : pd.Series 
        Target variable.

    Returns:
    -------
    float
        Model accuracy score.
    """
    return model.score(X, y)


def save_results(accuracy_ridge: float, accuracy_tree: float, output_path: str):
    """
    Save evaluation results to a CSV file.

    Parameters:
    ----------
    accuracy_ridge : float 
        Accuracy of the Ridge Regression model.
    accuracy_tree : float
        Accuracy of the Tree-based model.
    output_path : str 
        Path to save the results CSV file.
    
    Returns:
    -------
    None
    """
    results = pd.DataFrame(
        {"accuracy_ridge": [accuracy_ridge], "accuracy_tree": [accuracy_tree]}
    )
    results.to_csv(output_path, index=False)


def generate_prediction_plot(model, X, y, output_path):
    """
    Generate a scatter plot for actual vs predicted values.

    Parameters:
    ----------
    model : sklearn model
        Trained model or pipeline.
    X : pd.DataFrame 
        Feature set.
    y : pd.Series
        Target variable.
    output_path : str  
        Path to save the prediction plot.

    Returns:
    -------
    None
    """
    plot = PredictionErrorDisplay.from_estimator(
        model,
        X,
        y,
        kind="actual_vs_predicted",
        scatter_kwargs={"alpha": 0.12, "s": 10},
    )
    plot.figure_.savefig(output_path)


def main_logic(test_data_path: str, pipeline_ridge_path: str, pipeline_tree_path: str, 
               results_to: str, plot_to: str, seed: int = 123):
    """
    Core logic for evaluating the rental bike models.

    Parameters:
    ----------
    test_data_path : str 
        Path to the test data CSV file.
    pipeline_ridge_path : str  
        Path to the Ridge Regression pipeline.
    pipeline_tree_path : str  
        Path to the Tree-based model pipeline.
    results_to : str  
        Path to save the results CSV file.
    plot_to : str  
        Path to save the plots.
    seed : int
        Random seed for reproducibility.

    Returns:
    -------
    None
    """
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # Load test data and models
    test_data = load_data(test_data_path)
    ridge_model = load_pipeline(pipeline_ridge_path)
    tree_model = load_pipeline(pipeline_tree_path)

    # Prepare features and target
    X_test = test_data.drop("Rented Bike Count", axis=1)
    y_test = test_data["Rented Bike Count"]

    # Evaluate models
    accuracy_ridge = evaluate_model(ridge_model, X_test, y_test)
    accuracy_tree = evaluate_model(tree_model, X_test, y_test)

    # Save results
    save_results(accuracy_ridge, accuracy_tree, os.path.join(results_to, "test_scores.csv"))

    # Generate prediction plots
    generate_prediction_plot(
        ridge_model, X_test, y_test, os.path.join(plot_to, "prediction_error_ridge.png")
    )
    generate_prediction_plot(
        tree_model, X_test, y_test, os.path.join(plot_to, "prediction_error_tree.png")
    )