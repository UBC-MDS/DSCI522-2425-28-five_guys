from sklearn.model_selection import train_test_split

def split_data(df, test_size=0.3, random_state=123):
    """
    Splits the data into training and testing sets.
    Parameters:
        df (pd.DataFrame): The DataFrame to split
        test_size (float): Proportion of the dataset to include in the test split
        random_state (int): Random seed
    Returns:
        tuple: Training and testing DataFrames
    """
    return train_test_split(df, test_size=test_size, random_state=random_state)
