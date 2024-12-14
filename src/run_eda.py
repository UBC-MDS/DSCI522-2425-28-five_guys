import os
import altair as alt
import pandas as pd
import warnings
import altair_ally as aly


def run_eda(processed_training_data, plot_to, table_to):
    """
    Perform Exploratory Data Analysis (EDA) on the provided processed training data.

    Parameters:
    ----------
    processed_training_data : str
        Path to the processed training data CSV file.
    plot_to : str
        Path to the directory where the plots will be saved.
    table_to : str
        Path to the directory where the summary tables will be saved.
    
    Returns:
    -------
    None
    """

    # Suppress specific Altair deprecation warnings
    warnings.filterwarnings("ignore", category=alt.utils.deprecation.AltairDeprecationWarning)

    # Read only 100 data points
    df = pd.read_csv(processed_training_data).sample(100)
 
    
    # Check for missing values
    missing_values = df.isnull().sum()
    missing_values_table = pd.DataFrame({"Missing Values": missing_values})
    missing_values_table.to_csv(os.path.join(table_to, "test_missing_values.csv"), index=False)
    
    # Summary statistics
    summary_stats = df.describe()
    summary_stats_table = summary_stats.loc['mean':'max'].reset_index()
    summary_stats_table.to_csv(os.path.join(table_to, "test_summary_stats.csv"), index=False)
    
    # Plot distribution of rented bike count
    rented_bike_hist = alt.Chart(df).mark_bar().encode(
        alt.X('Rented Bike Count:Q', bin=True, title='Rented Bike Count'),
        alt.Y('count()', title='Frequency'),
        tooltip=['count()']
    ).properties(
        title='Distribution of Rented Bike Count',
        width=700,
        height=400
    )
    rented_bike_hist.save(os.path.join(plot_to, "test_rented_bike_count.png"), scale_factor=2.0)
    
    # Plot hourly average rented bike count
    hourly_avg_chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Hour:O', title='Hour of Day'),
        y=alt.Y('mean(Rented Bike Count):Q', title='Average Rented Bike Count'),
        tooltip=['Hour', 'mean(Rented Bike Count)']
    ).properties(
        title='Average Rented Bike Count by Hour',
        width=700,
        height=400
    )
    hourly_avg_chart.save(os.path.join(plot_to, "test_hourly_rental_count.png"), scale_factor=2.0)
    
    # Plot season average rented bike count
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
    season_avg_chart.save(os.path.join(plot_to, "test_season_rental_count.png"), scale_factor=2.0)
    
    # Plot scatterplot of bike count vs temperature for different seasons
    season_temp_chart = alt.Chart(df).mark_circle().encode(
        alt.X('Temperature:Q', title='Temperature (\u00b0C)'),
        alt.Y('Rented Bike Count:Q', title='Rented Bike Count'),
        color='Seasons:N',
        tooltip=['Temperature', 'Rented Bike Count', 'Seasons']
    ).properties(
        title='Number of bike rentals at different temperatures for different seasons',
        width=600,
        height=400
    )
    season_temp_chart.save(os.path.join(plot_to, "test_season_temp_count.png"), scale_factor=2.0)
    
    # Plot distribution of bike rentals between holidays and non-holidays
    holiday_dist_chart = alt.Chart(df).mark_boxplot().encode(
        alt.X('Holiday:N', title='Holiday'),
        alt.Y('Rented Bike Count:Q', title='Rented Bike Count'),
        color='Holiday:N',
        tooltip=['Holiday', 'Rented Bike Count']
    ).properties(
        title='Summary distribution of bike rentals between holidays and non-holidays',
        width=600,
        height=400
    )
    holiday_dist_chart.save(os.path.join(plot_to, "test_holiday_dist.png"), scale_factor=2.0)
    
    # Plot hourly bike graph per season
    hourly_season_chart = alt.Chart(df).mark_line().encode(
        x='Hour:O',
        y='mean(Rented Bike Count)',
        color='Seasons',
        tooltip=['Hour', 'mean(Rented Bike Count)']
    )
    hourly_season_chart.save(os.path.join(plot_to, "test_season_hourly.png"), scale_factor=2.0)
    
    # Plot correlation graph of all features
    corr_chart = aly.corr(df)
    corr_chart.save(os.path.join(plot_to, "test_corr_chart.png"), scale_factor=2.0)


