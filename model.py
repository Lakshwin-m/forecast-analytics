from keras.models import load_model

def load_trained_model(path="model/conv1d_model_1.keras"):
    """Loads the saved Conv1D model."""
    return load_model(path)
