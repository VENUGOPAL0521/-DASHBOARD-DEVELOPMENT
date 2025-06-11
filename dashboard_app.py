
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load dataset
df = pd.read_csv("sample_sales_data.csv", parse_dates=['Order Date'])

# Preprocessing
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.to_period('M').astype(str)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Sales Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Interactive Sales Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            options=[{"label": r, "value": r} for r in df['Region'].unique()],
            value=None,
            id="region-filter",
            placeholder="All Regions"
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            options=[{"label": y, "value": y} for y in sorted(df['Year'].unique())],
            value=None,
            id="year-filter",
            placeholder="All Years"
        ),
    ], style={'width': '25%', 'display': 'inline-block', 'marginLeft': '20px'}),

    dcc.Graph(id='sales-trend'),
    dcc.Graph(id='category-sales'),
    dcc.Graph(id='region-map')
])

# Callbacks
@app.callback(
    [Output('sales-trend', 'figure'),
     Output('category-sales', 'figure'),
     Output('region-map', 'figure')],
    [Input('region-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_dashboard(selected_region, selected_year):
    filtered_df = df.copy()
    if selected_region:
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]

    # Sales Trend Line Chart
    trend_fig = px.line(
        filtered_df.groupby('Month').sum().reset_index(),
        x='Month', y='Sales', title='Monthly Sales Trend'
    )

    # Category Sales Bar Chart
    category_fig = px.bar(
        filtered_df.groupby('Category').sum().reset_index(),
        x='Category', y='Sales', title='Sales by Product Category'
    )

    # Regional Profit Bar Chart
    region_fig = px.bar(
        filtered_df.groupby('Region').sum().reset_index(),
        x='Region', y='Profit', title='Profit by Region'
    )

    return trend_fig, category_fig, region_fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
