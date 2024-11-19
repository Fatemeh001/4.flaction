import lightningchart as lc
import pandas as pd
import numpy as np

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Processed.xlsx'
fcpi_data = pd.read_excel(file_path, sheet_name='fcpi_m')
ecpi_data = pd.read_excel(file_path, sheet_name='ecpi_m')
def_a_data = pd.read_excel(file_path, sheet_name='def_a')

countries = ['Bulgaria', 'Guinea', 'Turkey', 'Suriname', 'Ukraine', 
             'Nigeria', 'Kyrgyz Republic', 'Haiti', 'Ethiopia', 'Honduras']
years = [str(year) for year in range(2020, 2024)] 

inflation_data = {}
for country in countries:
    if country in def_a_data['Country'].values:
        country_data = (
            def_a_data[def_a_data['Country'] == country]
            .filter(regex='^' + '|^'.join(years))
            .iloc[0]
        )
        inflation_data[country] = country_data.tolist()
    else:
        print(f"Country '{country}' does not exist in the dataset.")
        exit()

energy_data = {}
for country in countries:
    if country in ecpi_data['Country'].values:
        monthly_data = ecpi_data[ecpi_data['Country'] == country]
        monthly_data.columns = monthly_data.columns.map(str)
        monthly_data = monthly_data.apply(pd.to_numeric, errors='coerce')  
        annual_data = monthly_data.groupby(lambda x: x[:4], axis=1).mean().iloc[0].tolist()
        annual_data = [annual_data[int(year) - 2020] for year in years]  
    else:
        print(f"Country '{country}' does not exist in the energy dataset.")
        exit()

food_data = {}
for country in countries:
    if country in fcpi_data['Country'].values:
        monthly_data = fcpi_data[fcpi_data['Country'] == country]
        monthly_data.columns = monthly_data.columns.map(str)
        monthly_data = monthly_data.apply(pd.to_numeric, errors='coerce') 
        annual_data = monthly_data.groupby(lambda x: x[:4], axis=1).mean().iloc[0].tolist()
        annual_data = [annual_data[int(year) - 2020] for year in years] 
    else:
        print(f"Country '{country}' does not exist in the food dataset.")
        exit()

def normalize(data, min_val, max_val):
    return [(value - min_val) / (max_val - min_val) for value in data]

min_inflation, max_inflation = min(map(min, inflation_data.values())), max(map(max, inflation_data.values()))
min_energy, max_energy = min(map(min, energy_data.values())), max(map(max, energy_data.values()))
min_food, max_food = min(map(min, food_data.values())), max(map(max, food_data.values()))

normalized_inflation = {k: normalize(v, min_inflation, max_inflation) for k, v in inflation_data.items()}
normalized_energy = {k: normalize(v, min_energy, max_energy) for k, v in energy_data.items()}
normalized_food = {k: normalize(v, min_food, max_food) for k, v in food_data.items()}

chart = lc.Chart3D(title="3D Scatter Plot: Inflation, Energy & Food Prices", theme=lc.Themes.Light)
chart.get_default_x_axis().set_title('Inflation (DEF_A)').set_interval(0, 1)
chart.get_default_y_axis().set_title('Energy Price (ECPI_M)').set_interval(0, 1)
chart.get_default_z_axis().set_title('Food Price (FCPI_M)').set_interval(0, 1)

for country in countries:
    scatter_series = chart.add_point_series()
    scatter_series.set_point_size(20)  
    scatter_series.add([
        {
            'x': normalized_inflation[country][i],
            'y': normalized_energy[country][i],
            'z': normalized_food[country][i],
        }
        for i in range(len(years))
    ])
    scatter_series.set_name(country)

chart.add_legend()

chart.open()
