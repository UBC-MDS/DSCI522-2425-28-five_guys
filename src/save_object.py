import pickle

def save_object(obj, filepath):
    """
    Saves an object to a file using pickle.
    Parameters:
        obj: The object to save
        filepath (str): The file path to save the object
    """
    with open(filepath, "wb") as f:
        pickle.dump(obj, f)
