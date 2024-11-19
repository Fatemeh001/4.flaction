import pandas as pd
import lightningchart as lc
import time
from geopy.geocoders import Nominatim
from pycountry_convert import country_name_to_country_alpha2, country_alpha2_to_continent_code

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/Processed.xlsx'
data = pd.read_excel(file_path, sheet_name='ecpi_m')

def get_continent(country_name):
    try:
        country_code = country_name_to_country_alpha2(country_name)
        continent_code = country_alpha2_to_continent_code(country_code)
        return {
            'AF': 'Africa',
            'AS': 'Asia',
            'EU': 'Europe',
            'NA': 'North America',
            'SA': 'South America',
            'OC': 'Oceania'
        }.get(continent_code, 'Unknown')
    except:
        return 'Unknown'

data['Continent'] = data['Country'].apply(get_continent)

data = data[data['Continent'] != 'Unknown']

def calculate_continent_growth_percentage(year, prev_year):
    try:
        current_year_columns = [col for col in data.columns if str(year) in str(col)]
        prev_year_columns = [col for col in data.columns if str(prev_year) in str(col)]
        
        if not current_year_columns or not prev_year_columns:
            return None

        data_grouped_current = data.groupby('Continent')[current_year_columns].mean().mean(axis=1)
        data_grouped_prev = data.groupby('Continent')[prev_year_columns].mean().mean(axis=1)

        growth_percentage = ((data_grouped_current - data_grouped_prev) / data_grouped_prev) * 100
        return growth_percentage
    except Exception as e:
        print(f"Error calculating growth percentage: {e}")
        return None

dashboard = lc.Dashboard(theme=lc.Themes.TurquoiseHexagon, rows=2, columns=3)

gauges = {}
row, col = 0, 0
for continent in ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']:
    gauges[continent] = dashboard.GaugeChart(row_index=row, column_index=col)
    gauges[continent].set_title(f"{continent}: Energy Price Index Growth (%)")
    gauges[continent].set_angle_interval(start=225, end=-45)
    gauges[continent].set_interval(start=-50, end=50)  # Percentage growth range
    gauges[continent].set_bar_thickness(20)
    gauges[continent].set_value_indicator_thickness(10)
    gauges[continent].set_value_label_font(30)

    gauges[continent].set_value_indicators([
        {'start': -50, 'end': -10, 'color': lc.Color('blue')},  
        {'start': -10, 'end': 0, 'color': lc.Color('orange')},
        {'start': 0, 'end': 10, 'color': lc.Color('yellow')}, 
        {'start': 10, 'end': 50, 'color': lc.Color('red')}  
    ])
    col += 1
    if col > 2: 
        col = 0
        row += 1

dashboard.open(live=True)

for year in range(2000, 2024):
    prev_year = year - 1
    continent_growth_percentage = calculate_continent_growth_percentage(year, prev_year)
    if continent_growth_percentage is not None:
        for continent, growth_percentage in continent_growth_percentage.items():
            if continent in gauges:
                gauges[continent].set_value(growth_percentage)
                gauges[continent].set_title(f"{continent}: Growth ({year}) (%)")
    print(f"Year: {year}, Growth (%): {continent_growth_percentage}")
    time.sleep(1)
