import plotly.express as px


def create_chart(df, chart_type, x_column, y_column=None):
    """
    Creates and returns a Plotly chart based on the selected chart type.
    """

    if chart_type == "Bar Chart":
        return px.bar(df, x=x_column, y=y_column)

    elif chart_type == "Line Chart":
        return px.line(df, x=x_column, y=y_column)

    elif chart_type == "Scatter Plot":
        return px.scatter(df, x=x_column, y=y_column)

    elif chart_type == "Histogram":
        return px.histogram(df, x=x_column)

    elif chart_type == "Box Plot":
        return px.box(df, x=x_column, y=y_column)
    
    elif chart_type == "Pie Chart":
        return px.pie(df, names=x_column)

    else:
        return None