def convert_to_csv(df):
    """
    Converts a DataFrame to CSV format for downloading.
    """

    return df.to_csv(index=False).encode("utf-8")