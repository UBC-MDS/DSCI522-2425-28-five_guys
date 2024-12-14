# eda.py
# date: 2024-12-05

import os
import click
import altair as alt
import pandas as pd
import altair_ally as aly
import warnings

# Suppress specific Altair deprecation warnings
warnings.filterwarnings("ignore", category=alt.utils.deprecation.AltairDeprecationWarning)

@click.command()
@click.option('--processed_training_data', type=str, help="Path to processed training data")
@click.option('--plot_to', type=str, help="Path to directory where the plots will be written to")
@click.option('--table_to', type=str, help="Path to directory where the tables will be written to")

def main(processed_training_data, plot_to, table_to):
    '''
    This script reads in the processed data and creates the tables and plots for EDA.
    '''
    df = pd.read_csv(processed_training_data)

    # Check for missing values
    missing_values = df.isnull().sum()
    missing_values_table = pd.DataFrame({"Missing Values": missing_values})
    missing_values_table.to_csv(os.path.join(table_to, "missing_values.csv"), index=False)

    # Summary statistics
    summary_stats = df.describe()
    summary_stats_table = summary_stats.loc['mean':'max'].reset_index()
    summary_stats_table.to_csv(os.path.join(table_to, "summary_stats.csv"), index=False)

    # plot distribution of rented bike count
    rented_bike_hist = alt.Chart(df).mark_bar().encode(
        alt.X('Rented Bike Count:Q', bin=True, title='Rented Bike Count'),
        alt.Y('count()', title='Frequency'),
        tooltip=['count()']
        ).properties(
            title='Distribution of Rented Bike Count',
            width=700,
            height=400
            )
    rented_bike_hist.save(os.path.join(plot_to, "rented_bike_count.png"),
                          scale_factor=2.0)
    
    # plot hourly average rented bike count
    hourly_avg_chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Hour:O', title='Hour of Day'),
        y=alt.Y('mean(Rented Bike Count):Q', title='Average Rented Bike Count'),
        tooltip=['Hour', 'mean(Rented Bike Count)']
        ).properties(
            title='Average Rented Bike Count by Hour',
            width=700,
            height=400
            )
    hourly_avg_chart.save(os.path.join(plot_to, "hourly_rental_count.png"),
                          scale_factor=2.0)
    
    # plot season average rented bike count
    season_avg_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Seasons:O', title='Season'),
        y=alt.Y('mean(Rented Bike Count):Q', title='Average Rented Bike Count'),
        color='Seasons',
        tooltip=['Seasons', 'mean(Rented Bike Count)']
        ).properties(
            title='Average Rented Bike Count by Season',
            width=700,
            height=400
        )
    season_avg_chart.save(os.path.join(plot_to, "season_rental_count.png"),
                          scale_factor=2.0)
    
    # plot scatterplot of bike count vs temperature for different seasons
    season_temp_chart = alt.Chart(df).mark_circle().encode(
        alt.X('Temperature:Q', title='Temperature (°C)'),
        alt.Y('Rented Bike Count:Q', title='Rented Bike Count'),
        color='Seasons:N',
        tooltip=['Temperature', 'Rented Bike Count', 'Seasons']
        ).properties(
            title='Number of bike rentals at different temperatures for different seasons',
            width=600,
            height=400
        )
    season_temp_chart.save(os.path.join(plot_to, "season_temp_count.png"),
                          scale_factor=2.0)
    
    # Plot distribution of bike rentals between holidays and non-holidays
    holiday_dist_chart = alt.Chart(df).mark_boxplot().encode(
        alt.X('Holiday:N', title='Holiday'),
        alt.Y('Rented Bike Count:Q', title='Rented Bike Count'),
        color='Holiday:N',
        tooltip=['Holiday', 'Rented Bike Count']
        ).properties(
            title='Summary distribution of bike rentals between holidays and non holidays',
            width=600,
            height=400
        )
    holiday_dist_chart.save(os.path.join(plot_to, "holiday_dist.png"),
                          scale_factor=2.0)
    
    # Plot hourly bike graph per season
    hourly_season_chart = alt.Chart(df).mark_line().encode(
        x='Hour:O',
        y='mean(Rented Bike Count)',
        color='Seasons',
        tooltip=['Hour', 'mean(Rented Bike Count)']
    )
    hourly_season_chart.save(os.path.join(plot_to, "season_hourly.png"),
                          scale_factor=2.0)
    
    # plot correlation graph of all features
    corr_chart = aly.corr(df)
    corr_chart.save(os.path.join(plot_to, "corr_chart.png"),
                          scale_factor=2.0)

if __name__ == '__main__':
    main()
