# fit_bike_usage_regressor.py
# date: 2024-12-05
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor

def fit_model(training_data, preprocessor, pipeline_to, seed):
    """
    Fits a rental bike regressor model (Ridge and Decision Tree) to the provided training data 
    and saves the resulting pipelines as pickle files.

    Parameters:
    ----------
    training_data : str
        Path to the CSV file containing the training data. The dataset should include a 
        column 'Rented Bike Count' which will be used as the target variable.
    preprocessor : str
        Path to the preprocessor pickle file that will be used to preprocess the training data.
    pipeline_to : str
        Path to the directory where the fitted pipelines will be saved as pickle files.
    seed : int
        Random seed used for reproducibility in model training and hyperparameter search.

    Returns:
    -------
    None
    """
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # read in data & preprocessor
    rental_bike_train = pd.read_csv(training_data)
    rental_bike_preprocessor = pickle.load(open(preprocessor, "rb"))

    # Ridge Regression Pipeline
    ridge_pipeline = make_pipeline(
        rental_bike_preprocessor,
        Ridge()
    )

    # Decision Tree Pipeline
    tree_pipeline = make_pipeline(
        rental_bike_preprocessor,
        DecisionTreeRegressor(random_state=42)
    )

    # Define parameter grids for RandomizedSearchCV
    ridge_param_grid = {
        'ridge__alpha': np.logspace(-3, 3, 10)
    }

    tree_param_grid = {
        'decisiontreeregressor__max_depth': [None, 10, 20, 30, 40],
        'decisiontreeregressor__min_samples_split': [2, 5, 10],
        'decisiontreeregressor__min_samples_leaf': [1, 2, 4]
    }

    # Perform RandomizedSearchCV for both pipelines
    ridge_search = RandomizedSearchCV(
        estimator=ridge_pipeline,
        param_distributions =  ridge_param_grid,
        cv = 10, n_iter = 10, random_state=seed)

    tree_search = RandomizedSearchCV(
        estimator=tree_pipeline,
        param_distributions =  tree_param_grid,
        cv = 10, n_iter = 10, random_state=seed)
        
    # Fit models
    ridge_fit = ridge_search.fit(rental_bike_train.drop(
    "Rented Bike Count", axis=1), rental_bike_train["Rented Bike Count"])
    tree_fit = tree_search.fit(rental_bike_train.drop(
    "Rented Bike Count", axis=1), rental_bike_train["Rented Bike Count"])


    with open(os.path.join(pipeline_to, "ridge_pipeline.pickle"), 'wb') as f:
        pickle.dump(ridge_fit, f)

    with open(os.path.join(pipeline_to, "tree_pipeline.pickle"), 'wb') as f:
        pickle.dump(tree_fit, f)

    return None

