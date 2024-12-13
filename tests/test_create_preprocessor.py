import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.create_preprocessor import create_preprocessor

def test_create_preprocessor():
    preprocessor = create_preprocessor()
    assert hasattr(preprocessor, "fit")
    assert hasattr(preprocessor, "transform")
