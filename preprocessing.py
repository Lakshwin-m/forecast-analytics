import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

def load_and_preprocess(csv_path, n_steps=24):  # <-- match model input
    """
    Loads dataset, scales, and creates sequences for time series forecasting.
    Args:
        csv_path (str): Path to dataset
        n_steps (int): Lookback window
    Returns:
        X, y, scaler
    """
    df = pd.read_csv(csv_path)

    # Pick the target column (second column in CSV)
    values = df.iloc[:, 1].values.reshape(-1, 1)

    # Scale data
    scaled = scaler.fit_transform(values)

    # Create sequences
    X, y = [], []
    for i in range(n_steps, len(scaled)):
        X.append(scaled[i-n_steps:i, 0])
        y.append(scaled[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # shape = (batch, 24, 1)
    return X, y, scaler
