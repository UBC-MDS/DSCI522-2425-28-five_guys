import pandas as pd
def clean_and_engineer_data(df):
    """
    Cleans and engineers features for the given DataFrame.
    Parameters:
        df (pd.DataFrame): The raw data
    Returns:
        pd.DataFrame: A cleaned and engineered DataFrame
    """
    # Rename columns
    df = df.rename(columns={
        'Temperature(°C)': 'Temperature',
        'Humidity(%)': 'Humidity',
        'Rainfall(mm)': 'Rainfall',
        'Snowfall (cm)': 'Snowfall',
        'Wind speed (m/s)': 'Wind speed',
        'Visibility (10m)': 'Visibility',
        'Solar Radiation (MJ/m2)': 'Radiation',
        'Dew point temperature(°C)': 'Dew point temperature'
    })
    # Convert the Date column to datetime and extract features
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Weekday'] = df['Date'].dt.weekday
    df.drop(['Date'], axis=1, inplace=True)
    # Convert to categorical
    df['Seasons'] = df['Seasons'].astype(str)
    # Binary encoding
    df['Holiday'] = df['Holiday'].apply(lambda x: 1 if x == "Holiday" else 0)
    df['Functioning Day'] = df['Functioning Day'].apply(lambda x: 1 if x == "Yes" else 0)
    return df