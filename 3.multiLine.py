import pandas as pd
import lightningchart as lc

# Load the license key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Processed.xlsx'

# List of countries to compare
countries = ["Albania", "Turkey", "Greece"]

# Load the dataset and filter for selected countries
data = pd.read_excel(file_path, sheet_name='fcpi_m')

# Prepare a dictionary to hold country data
country_data_dict = {}
for country in countries:
    country_data = data[data['Country'] == country].iloc[:, 5:]
    country_data = country_data.filter(regex='^2018|^2019|^2020|^2021|^2022|^2023')
    country_data = country_data.dropna(how='all')  # Remove rows with all NaN values
    country_data = country_data.T
    country_data.columns = [country]
    
    # Ensure the index is treated as a string
    country_data.index = country_data.index.astype(str)
    
    # Safely extract Year and Month
    country_data['Year'] = pd.to_numeric(country_data.index.str[:4], errors='coerce')
    country_data['Month'] = pd.to_numeric(country_data.index.str[4:6], errors='coerce')
    
    # Drop rows where Year or Month extraction fails
    country_data = country_data.dropna(subset=['Year', 'Month'])
    country_data['Year'] = country_data['Year'].astype(int)
    country_data['Month'] = country_data['Month'].astype(int)
    
    # Store processed data
    country_data_dict[country] = country_data

# Create a new chart
chart = lc.ChartXY(
    title="Multi-line Line Chart: Food Price Index (2018-2023)",
    theme=lc.Themes.Dark
)

# Add legend
legend = chart.add_legend()

# Add line series for each country
for country, country_data in country_data_dict.items():
    line_series = chart.add_line_series().set_name(country)
    x_values = country_data['Year'] + country_data['Month'] / 12  # Combine Year and Month for X-axis
    y_values = country_data[country]
    line_series.add(x_values, y_values)
    legend.add(line_series)

# Set axis titles
chart.get_default_x_axis().set_title('Year')
chart.get_default_y_axis().set_title('Food Price Index')

# Open the chart
chart.open()
