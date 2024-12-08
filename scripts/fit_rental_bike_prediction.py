# fit_bike_usage_regressor.py

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor


@click.command()
@click.option('--training-data', type=str, help="Path to training data")
@click.option('--preprocessor', type=str, help="Path to preprocessor object")
# @click.option('--columns-to-drop', type=str, help="Optional: columns to drop")
@click.option('--pipeline-to', type=str, help="Path to directory where the pipeline object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(training_data, preprocessor, pipeline_to, seed):
    '''Fits a rental bike classiier to the training data and saves the
    pipeline object.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # read in data & preprocessor
    rental_bike_train = pd.read_csv(training_data)
    rental_bike_preprocessor = pickle.load(open(preprocessor, "rb"))
    
    # if columns_to_drop:
    #     to_drop = pd.read_csv(columns_to_drop).feats_to_drop.tolist()
    #     rental_bike_train = rental_bike_train.drop(columns=to_drop)

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

if __name__ == '__main__':
    main()
