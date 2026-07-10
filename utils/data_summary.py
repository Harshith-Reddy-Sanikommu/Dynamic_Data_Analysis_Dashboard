import pandas as pd


def get_dataset_shape(df):
    """
    Returns the number of rows and columns.
    """
    return df.shape


def get_column_names(df):
    """
    Returns all column names.
    """
    return df.columns.tolist()


def get_column_types(df):
    """
    Returns the data type of each column.
    """
    return df.dtypes


def get_summary_statistics(df):
    """
    Returns summary statistics for the dataset.
    """
    return df.describe(include="all")


def get_missing_values(df):
    """
    Returns the number of missing values in each column.
    """
    return df.isnull().sum()