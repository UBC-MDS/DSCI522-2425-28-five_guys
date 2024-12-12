# evaluate_rental_bike_prediction.py
# date: 2024-12-05

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.metrics import PredictionErrorDisplay

@click.command()
@click.option('--test-data', type=str, help="Path to test data")
# @click.option('--columns-to-drop', type=str, help="Optional: columns to drop")
@click.option('--pipeline-from-ridge', type=str, help="Path to directory where the ridge fit pipeline object lives")
@click.option('--pipeline-from-tree', type=str, help="Path to directory where the tree fit pipeline object lives")
@click.option('--results-to', type=str, help="Path to directory where the plot will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)
@click.option('--plot_to', type=str, help="Path to directory where the plots will be written to")
def main(test_data, plot_to, pipeline_from_ridge,pipeline_from_tree,results_to, seed):
    '''Evaluates the rental bike regressor on the test data 
    and saves the evaluation results.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # read in data & cancer_fit (pipeline object)
    rental_bike_test = pd.read_csv(test_data)
    # if columns_to_drop:
    #     to_drop = pd.read_csv(columns_to_drop).feats_to_drop.tolist()
    #     rental_bike_test = rental_bike_test.drop(columns=to_drop)
    with open(pipeline_from_ridge, 'rb') as f:
        rental_bike_fit_ridge = pickle.load(f)
    with open(pipeline_from_tree, 'rb') as f:
        rental_bike_fit_tree = pickle.load(f)

    # Compute accuracy
    accuracy_ridge = rental_bike_fit_ridge.score(
        rental_bike_test.drop("Rented Bike Count", axis=1),
        rental_bike_test["Rented Bike Count"]
    )

    accuracy_tree = rental_bike_fit_tree.score(
    rental_bike_test.drop("Rented Bike Count", axis=1),
    rental_bike_test["Rented Bike Count"]
    )

    test_scores = pd.DataFrame({'accuracy_ridge': [accuracy_ridge], 'accuracy_tree': [accuracy_tree]})
    test_scores.to_csv(os.path.join(results_to, "test_scores.csv"), index=False)

    # Plotting scatter plot for predicted value vs actual value on test set
    plot_pred_ridge = PredictionErrorDisplay.from_estimator(
        rental_bike_fit_ridge,
        rental_bike_test.drop("Rented Bike Count", axis=1),
        rental_bike_test["Rented Bike Count"],
        kind='actual_vs_predicted',
        scatter_kwargs={'alpha': 0.12, 's': 10}
    )

    plot_pred_ridge.figure_.savefig(os.path.join(plot_to, "prediction_error_ridge.png"))
    

    # Plotting scatter plot for predicted value vs actual value on test set
    plot_pred_tree = PredictionErrorDisplay.from_estimator(
        rental_bike_fit_tree,
        rental_bike_test.drop("Rented Bike Count", axis=1),
        rental_bike_test["Rented Bike Count"],
        kind='actual_vs_predicted',
        scatter_kwargs={'alpha': 0.12, 's': 10}
    )

    plot_pred_tree.figure_.savefig(os.path.join(plot_to, "prediction_error_tree.png"))
    


if __name__ == '__main__':
    main()