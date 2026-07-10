import streamlit as st
import pandas as pd
from utils.file_handler import load_data
from utils.data_summary import (
    get_dataset_shape,
    get_column_names,
    get_column_types,
    get_summary_statistics,
    get_missing_values,
)

from utils.visualization import create_chart
from utils.filters import filter_data
from utils.download import convert_to_csv



# Page Configuration
st.set_page_config(
    page_title="Dynamic Data Analysis Dashboard",
    layout="wide"
)

st.title("📊 Dynamic Data Analysis Dashboard")
st.write("Upload a CSV file and analyze your data.")


# File Upload
uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    # Load Dataset
    df = load_data(uploaded_file)

    st.success("CSV file uploaded successfully!")
    # Dataset Preview
    st.header("Dataset Preview")
    st.dataframe(df)

    # Dataset Information
    st.header("Dataset Information")

    rows, columns = get_dataset_shape(df)

    st.write("**Number of Rows:**", rows)
    st.write("**Number of Columns:**", columns)

    st.subheader("Column Names")
    st.write(get_column_names(df))

    st.subheader("Column Data Types")
    st.write(get_column_types(df))
    # Summary Statistics
    st.header("Summary Statistics")

    summary = get_summary_statistics(df)
    st.dataframe(summary)

    # Missing Value Analysis
    st.header("Missing Value Analysis")

    missing_values = get_missing_values(df)
    st.dataframe(missing_values)

    # Data Filtering
    st.header("Filter Data")

    filter_column = st.selectbox(
        "Select Column",
        get_column_names(df)
    )

    if not pd.api.types.is_numeric_dtype(df[filter_column]):

        unique_values = df[filter_column].dropna().unique()

        selected_value = st.selectbox(
            "Select Value",
            unique_values
        )

        filtered_df = filter_data(
            df,
            filter_column,
            "Equals",
            selected_value
        )

    else:

        condition = st.selectbox(
            "Select Condition",
            ["Equals", "Greater Than", "Less Than", "Between"]
        )

        if condition == "Between":

            value1 = st.number_input("Minimum Value")

            value2 = st.number_input("Maximum Value")

            filtered_df = filter_data(
                df,
                filter_column,
                condition,
                value1,
                value2
            )

        else:

            value = st.number_input("Enter Value")

            filtered_df = filter_data(
                df,
                filter_column,
                condition,
                value
            )

    st.subheader("Filtered Dataset")

    st.dataframe(filtered_df)

    # Data Visualization
    st.header("Data Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Bar Chart",
            "Line Chart",
            "Scatter Plot",
            "Histogram",
            "Box Plot",
            "Pie Chart"
        ]
    )

    x_column = st.selectbox(
        "Select X-axis",
        filtered_df.columns
    )

    if chart_type == "Histogram":

        figure = create_chart(
            filtered_df,
            chart_type,
            x_column
        )
    elif chart_type == "Pie Chart":

        figure = create_chart(
            filtered_df,
            chart_type,
            x_column
        )
    else:

        numeric_columns = filtered_df.select_dtypes(
            include="number"
        ).columns.tolist()

        if len(numeric_columns) > 0:

            y_column = st.selectbox(
                "Select Y-axis",
                numeric_columns
            )

            figure = create_chart(
                filtered_df,
                chart_type,
                x_column,
                y_column
            )

        else:

            st.warning("No numeric columns available for the selected chart.")
            figure = None

    if figure is not None:
        st.plotly_chart(figure, use_container_width=True)

    # Download Dataset
    st.header("Download Cleaned Dataset")

    csv_file = convert_to_csv(filtered_df)

    st.download_button(
        label="Download CSV",
        data=csv_file,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

else:

    st.info("Please upload a CSV file to begin.")