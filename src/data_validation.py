import pandas as pd
import pandera as pa
import numpy as np

def data_validation(bike_dataframe):
    """
    Validates the input rental bike data in the form of a pandas dataframe
    and returns the validated dataframe.

    This function checks the columns in the input dataframe to ensure that
    they are of the correct range and type. It also ensures that there is
    no duplicated or empty rows.

    Parameters
    ---------
    bike_dataframe : pandas.DataFrame
        The DataFrame containing rental bike related data, it includes columns 
        such as 'hour of the day', 'temperature', 'day of the week', 'humidity',
        and other related weather measurements. The data is validated based on 
        specific criteria for each column. 

    Returns
    ----------
    pandas.DataFrame
        The validated DataFrame that conforms to the specified schema.
    
    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not conform to the specified schema (e.g.,
        incorrect data typees, duplicate rows, or empty rows)
    
    Notes
    -----
    The following columns are validated:
        - 'Date': Values must be string
        - 'Seasons': Values must be either "Winter", "Summer", "Autumn", or "Spring"
        - 'Holiday': Values must be either "Holiday" or "No Holiday"
        - "Functioning Day": Values must be either "Yes" or "No"
        - Additional checks to ensure there is no duplicate or completely empty rows
    """
    if not isinstance(bike_dataframe, pd.DataFrame):
        raise TypeError("Input must be a pandas Dataframe")
    if bike_dataframe.empty:
        raise ValueError("Dataframe must contain observations.")

    # Define Pandera schema
    schema = pa.DataFrameSchema(
        {
            "Date": pa.Column(str),
            "Rented Bike Count": pa.Column(int, pa.Check.between(0, np.inf)),
            "Hour": pa.Column(int, pa.Check.between(0, 23)),
            "Temperature(°C)": pa.Column(float),
            "Humidity(%)": pa.Column(int, pa.Check.between(0, 100)),
            "Wind speed (m/s)": pa.Column(float),
            "Visibility (10m)": pa.Column(int),
            "Dew point temperature(°C)": pa.Column(float),
            "Solar Radiation (MJ/m2)": pa.Column(float),
            "Rainfall(mm)": pa.Column(float,
                                      pa.Check(lambda s: s.isna().mean() <= 0.05, element_wise=False,
                                               error="Too many null values in 'Rainfall(mm)' column."),
                                      nullable=True),
            "Snowfall (cm)": pa.Column(float),
            "Seasons": pa.Column(str, pa.Check.isin(["Winter", "Summer", "Autumn", "Spring"])),
            "Holiday": pa.Column(str, pa.Check.isin(["Holiday", "No Holiday"])),
            "Functioning Day": pa.Column(str, pa.Check.isin(["Yes", "No"]))
        },
        checks=[
            pa.Check(lambda bike_dataframe: ~bike_dataframe.duplicated().any(), error="Duplicate rows found."),
            pa.Check(lambda bike_dataframe: ~(bike_dataframe.isna().all(axis=1)).any(), error="Empty rows found.")
        ]
    )

    # Validate schema
    bike_dataframe = schema.validate(bike_dataframe, lazy=True).drop_duplicates().dropna(how="all")

    return bike_dataframe