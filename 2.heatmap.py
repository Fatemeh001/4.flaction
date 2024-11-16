import pandas as pd
import numpy as np
import lightningchart as lc

# Load the license key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Processed.xlsx'

selected_country = "Albania"
data = pd.read_excel(file_path, sheet_name='fcpi_m')
selected_country_data = data[data['Country'] == selected_country].iloc[:, 5:]

# Extract data for years 2000 to 2023
data_selected_years = selected_country_data.filter(regex='^2000|^2001|^2002|^2003|^2004|^2005|^2006|^2007|^2008|^2009|^2010|^2011|^2012|^2013|^2014|^2015|^2016|^2017|^2018|^2019|^2020|^2021|^2022|^2023')
data_selected_years.columns = [str(col) for col in data_selected_years.columns]

# Convert data to a suitable format
data_selected_years_t = data_selected_years.T
data_selected_years_t.columns = ['Index Value']
data_selected_years_t['Year'] = data_selected_years_t.index.str[:4].astype(int)
data_selected_years_t['Month'] = data_selected_years_t.index.str[4:6].astype(int)

# Pivot the data for the heatmap
heatmap_data = data_selected_years_t.pivot(index="Month", columns="Year", values="Index Value").fillna(0).values

# Convert years to timestamps
years = data_selected_years_t['Year'].unique()
years_ms = [int(pd.Timestamp(year=year, month=1, day=1).timestamp() * 1000) for year in years]

# Create a new chart
chart = lc.ChartXY(
    title=f"Food Price Index Heatmap for {selected_country} (2000-2023)",
    theme=lc.Themes.Dark
)

# Create the heatmap grid series
grid_size_x, grid_size_y = heatmap_data.shape
heatmap_series = chart.add_heatmap_grid_series(
    columns=grid_size_x,
    rows=grid_size_y
)

# Set the start, end, and step positions for the heatmap
heatmap_series.set_start(x=years_ms[0], y=1)  # Start Y at 1 (January)
heatmap_series.set_end(x=years_ms[-1], y=12)  # End Y at 12 (December)
heatmap_series.set_step(x=(years_ms[-1] - years_ms[0]) / grid_size_x, y=1)

# Enable interpolation and set intensity values from heatmap_data
heatmap_series.set_intensity_interpolation(True)
heatmap_series.invalidate_intensity_values(heatmap_data.tolist())

# Hide wireframe
heatmap_series.hide_wireframe()

# Define a custom color lookup table for the heatmap
heatmap_series.set_palette_coloring([
    {"value": np.min(heatmap_data), "color": lc.Color(0, 0, 255)},  # Blue for minimum
    {"value": np.max(heatmap_data), "color": lc.Color(255, 0, 0)}   # Red for maximum
])

# Set axis titles
chart.get_default_x_axis().set_title('Year')
chart.get_default_y_axis().set_title('Month')

# Format the X-axis to use years
x_axis = chart.get_default_x_axis()
x_axis.set_tick_strategy('DateTime', utc=True)

# Format the Y-axis to show only positive integers (1 to 12 for months)
y_axis = chart.get_default_y_axis()
y_axis.set_interval(1, 12, 1)  # Start at 1, end at 12, step of 1

# Add a legend
chart.add_legend(data=heatmap_series).set_title('Index Intensity')

# Open the chart
chart.open()
