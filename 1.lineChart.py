# import pandas as pd
# import lightningchart as lc


# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the dataset
# file_path = 'Processed.xlsx'
# df = pd.read_excel(file_path, sheet_name=0)

# # Define the list of countries
# countries = ['United States', 'Germany', 'India', 'China', 'Bangladesh']

# # Filter the data for the selected countries
# selected_data = df[df['Country'].isin(countries)]

# # Prepare data for each country
# country_data_list = {}
# for country in countries:
#     country_data = selected_data[selected_data['Country'] == country].iloc[:, 5:].T
#     country_data.columns = [country]
#     country_data.index.name = 'Year'
#     country_data.reset_index(inplace=True)
#     country_data['Year'] = pd.to_numeric(country_data['Year'], errors='coerce')
#     country_data.set_index('Year', inplace=True)
#     country_data[country] = pd.to_numeric(country_data[country], errors='coerce')
    
#     # Use cubic spline interpolation for smoother data
#     country_data = country_data.reindex(range(country_data.index.min(), country_data.index.max() + 1))
#     country_data[country] = country_data[country].interpolate(method='spline', order=3).fillna(method='bfill').fillna(method='ffill')
    
#     country_data_list[country] = country_data

# # Create the LightningChart and set the theme and title
# chart = lc.ChartXY(
#     theme=lc.Themes.Light,
#     title='Food Price Index Over Time for Selected Countries'
# )

# # Add the legend to the chart
# legend = chart.add_legend()

# # Add line series for each country
# for country, data in country_data_list.items():
#     line_series = chart.add_line_series().set_name(country)
#     x_values = list(data.index)  # Years
#     y_values = list(data[country])  # Food Price Index values
#     line_series.add(x_values, y_values)
#     legend.add(line_series)  # Attach each series to the legend

# # Open the chart with the legend
# chart.open()




import lightningchart as lc
import pandas as pd


with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)


file_path = 'Processed.xlsx'

selected_country = "Albania"
data = pd.read_excel(file_path, sheet_name='fcpi_m')
selected_country_data = data[data['Country'] == selected_country].iloc[:, 5:]


data_last_5_years = selected_country_data.filter(regex='^2018|^2019|^2020|^2021|^2022|^2023')
data_last_5_years.columns = [str(col) for col in data_last_5_years.columns]


data_last_5_years_t = data_last_5_years.T
data_last_5_years_t.columns = ['Index Value']
data_last_5_years_t['Year'] = data_last_5_years_t.index.str[:4].astype(int)
data_last_5_years_t['Month'] = data_last_5_years_t.index.str[4:6].astype(int)


chart = lc.ChartXY(
    theme=lc.Themes.Black,
    title=f"Food Price Index for {selected_country} (2018–2023)"
)


legend = chart.add_legend()


for year in range(2018, 2024):
    year_data = data_last_5_years_t[data_last_5_years_t['Year'] == year]
    x_values = list(year_data['Month'])
    y_values = list(year_data['Index Value'])
    
    line_series = chart.add_line_series().set_name(str(year))
    line_series.add(x_values, y_values)
    legend.add(line_series)  

chart.open()