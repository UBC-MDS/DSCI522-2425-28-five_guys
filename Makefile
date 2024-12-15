# Seoul Bike Sharing Demand Data Pipeline
# date: 2024-12-14
.PHONY: all clean

# Runs the entire pipeline and generates both HTML and PDF reports
all: report/rental_bike_prediction.html report/rental_bike_prediction.pdf

# Downloads raw data from UCI and writes it to the data/raw directory
data/raw/SeoulBikeData.csv: scripts/data_loading_n_validation.py
	python scripts/data_loading_n_validation.py \
	    --url="https://archive.ics.uci.edu/static/public/560/seoul+bike+sharing+demand.zip" \
	    --write_to=data/raw

# Splits and preprocesses the raw data into training and testing sets
data/processed/bike_train.csv \
data/processed/bike_test.csv \
results/models/bike_preprocessor.pickle: scripts/split_n_preprocessing.py \
data/raw/SeoulBikeData.csv
	python scripts/split_n_preprocessing.py \
	    --raw_data=data/raw/SeoulBikeData.csv \
	    --data_to=data/processed \
	    --preprocessor_to=results/models \
	    --seed=522

# Performs Exploratory Data Analysis (EDA) and generates plots and tables
results/tables/missing_values.csv \
results/tables/summary_stats.csv \
results/figures/rented_bike_count.png \
results/figures/hourly_rental_count.png \
results/figures/season_rental_count.png \
results/figures/season_temp_count.png \
results/figures/holiday_dist.png \
results/figures/season_hourly.png \
results/figures/corr_chart.png: scripts/eda.py data/processed/bike_train.csv
	python scripts/eda.py \
		--processed_training_data=data/processed/bike_train.csv \
		--plot_to=results/figures --table_to=results/tables

# Fits the Ridge and Tree regression model for rental bike prediction
results/models/ridge_pipeline.pickle \
results/models/tree_pipeline.pickle: scripts/fit_rental_bike_prediction.py data/processed/bike_train.csv results/models/bike_preprocessor.pickle
	python scripts/fit_rental_bike_prediction.py \
		--training-data=data/processed/bike_train.csv \
		--preprocessor=results/models/bike_preprocessor.pickle \
		--pipeline-to=results/models \
		--seed=522


# Evaluates the rental bike prediction models on the test data
results/figures/prediction_error_ridge.png \
results/figures/prediction_error_tree.png \
results/tables/test_scores.csv: scripts/evaluate_rental_bike_prediction.py \
data/processed/bike_test.csv \
results/models/ridge_pipeline.pickle \
results/models/tree_pipeline.pickle
	python scripts/evaluate_rental_bike_prediction.py \
		--test-data=data/processed/bike_test.csv \
		--pipeline-from-ridge=results/models/ridge_pipeline.pickle \
		--pipeline-from-tree=results/models/tree_pipeline.pickle \
		--results-to=results/tables \
		--seed=522 \
		--plot_to=results/figures

report/rental_bike_prediction.html \
report/rental_bike_prediction.pdf: report/rental_bike_prediction.qmd \
report/references.bib \
results/tables/test_scores.csv \
results/tables/summary_stats.csv \
results/models/ridge_pipeline.pickle \
results/models/tree_pipeline.pickle \
results/figures/prediction_error_ridge.png \
results/figures/prediction_error_tree.png
	quarto render report/rental_bike_prediction.qmd --to html
	quarto render report/rental_bike_prediction.qmd --to pdf

# Removes all generated outputs from the data pipeline

clean-dats :
	rm -rf data/raw/*
	rm -r data/processed/bike_train.csv \
			data/processed/bike_test.csv

clean-figs :
	rm -f results/figures/rented_bike_count.png \
			results/figures/hourly_rental_count.png \
			results/figures/season_rental_count.png \
			results/figures/season_temp_count.png \
			results/figures/holiday_dist.png \
			results/figures/season_hourly.png \
			results/figures/prediction_error_ridge.png \
			results/figures/prediction_error_tree.png

clean-tables :
	rm -f results/tables/summary_stats.csv \
			results/tables/missing_values.csv \
			results/tables/test_scores.csv

clean models :
	rm -f results/models/ridge_pipeline.pickle \
			results/models/tree_pipeline.pickle 

clean:
	rm -rf data/raw/*
	rm -r data/processed/bike_train.csv \
			data/processed/bike_test.csv \
			results/models/bike_preprocessor.pickle \
	rm -f results/figures/rented_bike_count.png \
			results/figures/hourly_rental_count.png \
			results/figures/season_rental_count.png \
			results/figures/season_temp_count.png \
			results/figures/holiday_dist.png \
			results/figures/season_hourly.png \
			results/figures/prediction_error_ridge.png \
			results/figures/prediction_error_tree.png \
	rm -f results/tables/summary_stats.csv \
			results/tables/missing_values.csv \
			results/tables/test_scores.csv
	rm -f results/models/ridge_pipeline.pickle \
			results/models/tree_pipeline.pickle 
	rm -rf report/rental_bike_prediction.html \
			report/rental_bike_prediction.pdf \
			report/rental_bike_prediction_files
