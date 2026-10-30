
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


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Data Analytics Studio",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

def load_css():
    try:
        with open("style.css", "r", encoding="utf-8") as file:
            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        st.warning("style.css not found. Keep it beside app.py.")


load_css()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="top-label">
        <span class="live-dot"></span>
        INTERACTIVE DATA INTELLIGENCE PLATFORM
    </div>
    <div class="hero">
        <div class="hero-content">
            <div class="hero-tag">DATA ANALYTICS · VISUALIZATION · INSIGHTS</div>
            <h1>Make your data<br><span>tell a story.</span></h1>
            <p>
                Transform raw CSV files into meaningful insights.
                Explore datasets, discover patterns, filter records,
                and visualize information in one workspace.
            </p>
        </div>
        <div class="hero-decoration">
            <div class="chart-symbol">▥</div>
            <div class="decoration-caption">DATA /  ANALYZE /  DISCOVER</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.markdown(
    """
    <div class="section-heading">
        <div class="section-number">01 / DATA SOURCE</div>
        <h2>Import your dataset</h2>
        <p>Upload a CSV file to begin your analysis.</p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"],
    help="Select a CSV file from your computer.",
    key="csv_uploader"
)


# --------------------------------------------------
# MAIN ANALYSIS
# --------------------------------------------------

if uploaded_file is not None:

    try:
        df = load_data(uploaded_file)

        if df is None or df.empty:
            st.warning("The uploaded CSV file contains no data.")

        else:

            st.success("Dataset uploaded successfully!")

            # ------------------------------------------
            # DATASET OVERVIEW
            # ------------------------------------------

            rows, columns = get_dataset_shape(df)
            missing_values = get_missing_values(df)

            missing_count = 0
            if isinstance(missing_values, pd.DataFrame):
                if "Missing Values" in missing_values.columns:
                    missing_count = int(
                        missing_values["Missing Values"].sum()
                    )
                else:
                    missing_count = int(df.isnull().sum().sum())
            else:
                missing_count = int(df.isnull().sum().sum())

            complete_cells = rows * columns - missing_count
            completeness = (
                (complete_cells / (rows * columns)) * 100
                if rows * columns > 0 else 0
            )

            st.markdown(
                """
                <div class="section-heading">
                    <div class="section-number">02 / DATA OVERVIEW</div>
                    <h2>Dataset at a glance</h2>
                    <p>A quick overview of your uploaded data.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            metric1, metric2, metric3, metric4 = st.columns(4)

            with metric1:
                st.metric(
                    "Total Records",
                    f"{rows:,}",
                    help="Number of rows in your dataset."
                )

            with metric2:
                st.metric(
                    "Total Columns",
                    f"{columns:,}",
                    help="Number of columns in your dataset."
                )

            with metric3:
                st.metric(
                    "Missing Values",
                    f"{missing_count:,}",
                    help="Total missing cells."
                )

            with metric4:
                st.metric(
                    "Data Completeness",
                    f"{completeness:.1f}%"
                )

            # ------------------------------------------
            # DATASET PREVIEW
            # ------------------------------------------

            st.markdown(
                """
                <div class="section-heading">
                    <div class="section-number">03 / EXPLORE</div>
                    <h2>Dataset preview</h2>
                    <p>Inspect the records and understand your dataset.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.dataframe(
                df,
                use_container_width=True,
                height=350
            )

            # ------------------------------------------
            # DATASET INFORMATION
            # ------------------------------------------

            with st.expander("VIEW DATASET STRUCTURE", expanded=False):

                info_col1, info_col2 = st.columns(2)

                with info_col1:
                    st.markdown("#### Column Names")
                    st.write(get_column_names(df))

                with info_col2:
                    st.markdown("#### Column Data Types")
                    st.write(get_column_types(df))

            # ------------------------------------------
            # SUMMARY STATISTICS
            # ------------------------------------------

            st.markdown(
                """
                <div class="section-heading">
                    <div class="section-number">04 / STATISTICS</div>
                    <h2>Summary statistics</h2>
                    <p>Understand the statistical properties of your data.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            summary = get_summary_statistics(df)

            st.dataframe(
                summary,
                use_container_width=True
            )

            # ------------------------------------------
            # MISSING VALUE ANALYSIS
            # ------------------------------------------

            st.markdown(
                """
                <div class="section-heading">
                    <div class="section-number">05 / DATA QUALITY</div>
                    <h2>Missing value analysis</h2>
                    <p>Identify incomplete columns in your dataset.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.dataframe(
                missing_values,
                use_container_width=True
            )

            # ------------------------------------------
            # DATA FILTERING
            # ------------------------------------------

            st.markdown(
                """
                <div class="section-heading">
                    <div class="section-number">06 / FILTER</div>
                    <h2>Explore specific records</h2>
                    <p>Filter your dataset using column values and conditions.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            filter_col1, filter_col2 = st.columns(2)

            column_names = get_column_names(df)

            with filter_col1:
                filter_column = st.selectbox(
                    "Select column",
                    column_names,
                    key="filter_column"
                )

            filtered_df = df.copy()

            if not pd.api.types.is_numeric_dtype(df[filter_column]):

                unique_values = df[filter_column].dropna().unique()

                if len(unique_values) > 0:

                    with filter_col2:
                        selected_value = st.selectbox(
                            "Select value",
                            unique_values,
                            key="filter_value"
                        )

                    filtered_df = filter_data(
                        df,
                        filter_column,
                        "Equals",
                        selected_value
                    )

                else:
                    st.info("This column does not contain filterable values.")

            else:

                with filter_col2:
                    condition = st.selectbox(
                        "Select condition",
                        [
                            "Equals",
                            "Greater Than",
                            "Less Than",
                            "Between"
                        ],
                        key="filter_condition"
                    )

                if condition == "Between":

                    min_value = float(df[filter_column].min())
                    max_value = float(df[filter_column].max())

                    value_col1, value_col2 = st.columns(2)

                    with value_col1:
                        value1 = st.number_input(
                            "Minimum value",
                            value=min_value,
                            key="minimum_value"
                        )

                    with value_col2:
                        value2 = st.number_input(
                            "Maximum value",
                            value=max_value,
                            key="maximum_value"
                        )

                    filtered_df = filter_data(
                        df,
                        filter_column,
                        condition,
                        value1,
                        value2
                    )

                else:

                    value = st.number_input(
                        "Enter value",
                        key="filter_number"
                    )

                    filtered_df = filter_data(
                        df,
                        filter_column,
                        condition,
                        value
                    )

            st.markdown(
                '<div class="filter-result-label">FILTERED DATASET</div>',
                unsafe_allow_html=True
            )

            st.caption(
                f"Showing {len(filtered_df):,} of {len(df):,} records."
            )

            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=300
            )

            # ------------------------------------------
            # DATA VISUALIZATION
            # ------------------------------------------

            st.markdown(
                """
                <div class="section-heading">
                    <div class="section-number">07 / VISUALIZE</div>
                    <h2>Discover patterns visually</h2>
                    <p>Choose a chart type and explore your data.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if not filtered_df.empty:

                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    chart_type = st.selectbox(
                        "Select chart type",
                        [
                            "Bar Chart",
                            "Line Chart",
                            "Scatter Plot",
                            "Histogram",
                            "Box Plot",
                            "Pie Chart"
                        ],
                        key="chart_type"
                    )

                with chart_col2:
                    x_column = st.selectbox(
                        "Select X-axis",
                        filtered_df.columns.tolist(),
                        key="x_column"
                    )

                figure = None

                if chart_type in ["Histogram", "Pie Chart"]:

                    figure = create_chart(
                        filtered_df,
                        chart_type,
                        x_column
                    )

                else:

                    numeric_columns = filtered_df.select_dtypes(
                        include="number"
                    ).columns.tolist()

                    if numeric_columns:

                        y_column = st.selectbox(
                            "Select Y-axis",
                            numeric_columns,
                            key="y_column"
                        )

                        figure = create_chart(
                            filtered_df,
                            chart_type,
                            x_column,
                            y_column
                        )

                    else:
                        st.warning(
                            "No numeric columns available for this chart."
                        )

                if figure is not None:
                    st.plotly_chart(
                        figure,
                        use_container_width=True,
                        theme="streamlit"
                    )

            else:
                st.warning(
                    "No records match your selected filter. "
                    "Change the filter to visualize data."
                )

            # ------------------------------------------
            # DOWNLOAD
            # ------------------------------------------

            st.markdown(
                """
                <div class="section-heading">
                    <div class="section-number">08 / EXPORT</div>
                    <h2>Export your results</h2>
                    <p>Download the filtered dataset for further use.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            csv_file = convert_to_csv(filtered_df)

            st.download_button(
                label="DOWNLOAD CLEANED DATASET  ↓",
                data=csv_file,
                file_name="cleaned_dataset.csv",
                mime="text/csv",
                use_container_width=True
            )

    except Exception as error:
        st.error(f"An error occurred while analyzing the dataset: {error}")

else:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">▤</div>
            <h3>Your analysis workspace is waiting.</h3>
            <p>
                Upload a CSV file above to explore records,
                inspect statistics, filter information,
                and create interactive visualizations.
            </p>
            <div class="empty-caption">
                SUPPORTED FORMAT · CSV
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="main-footer">
        <div class="footer-brand">DATA / STUDIO</div>
        <div class="footer-caption">
            TURN RAW DATA INTO MEANINGFUL INSIGHTS.
        </div>
        <div class="footer-bottom">
            DYNAMIC DATA ANALYSIS DASHBOARD · BUILT WITH STREAMLIT
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
