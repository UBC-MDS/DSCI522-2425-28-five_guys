from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer

def create_preprocessor():
    """
    Creates a column transformer for data preprocessing.
    Returns:
        sklearn.compose.ColumnTransformer: A preprocessor object
    """
    preprocessor = make_column_transformer(
        (OneHotEncoder(sparse_output=False), ['Hour', 'Seasons', 'Year', 'Month', 'Day']),
        ("drop", ['Dew point temperature']),
        remainder=StandardScaler()
    )
    return preprocessor
