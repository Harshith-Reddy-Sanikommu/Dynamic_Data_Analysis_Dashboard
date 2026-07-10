import pandas as pd


def filter_data(df, column, condition, value1, value2=None):
    """
    Filters the DataFrame based on the selected column and condition.
    """

    if column is None or condition is None:
        return df

    if pd.api.types.is_numeric_dtype(df[column]):

        if condition == "Equals":
            return df[df[column] == value1]

        elif condition == "Greater Than":
            return df[df[column] > value1]

        elif condition == "Less Than":
            return df[df[column] < value1]

        elif condition == "Between":
            return df[(df[column] >= value1) & (df[column] <= value2)]

    else:

        if value1 is None:
            return df

        return df[df[column] == value1]

    return df