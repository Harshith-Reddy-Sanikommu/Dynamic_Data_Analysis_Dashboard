import pandas as pd


def load_data(uploaded_file):
    """
    Loads a CSV file and returns a Pandas DataFrame.
    """

    if uploaded_file is None:
        return None

    try:
        df = pd.read_csv(uploaded_file)
        return df

    except Exception as e:
        raise Exception(f"Error loading CSV file: {e}")