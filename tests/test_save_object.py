import os
import pickle
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.save_object import save_object

def test_save_object(tmpdir):
    obj = {"key": "value"}
    filepath = os.path.join(tmpdir, "test.pkl")
    save_object(obj, filepath)

    with open(filepath, "rb") as f:
        loaded_obj = pickle.load(f)

    assert loaded_obj == obj
