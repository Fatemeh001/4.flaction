
import pandas as pd
import lightningchart as lc
import time

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Processed.xlsx'
data = pd.read_excel(file_path, sheet_name='fcpi_m')

continent_mapping = {
    "Afghanistan": "Asia", "Albania": "Europe", "Austria": "Europe",
    "Azerbaijan": "Asia", "Belgium": "Europe", "Bulgaria": "Europe",
    "Bosnia and Herzegovina": "Europe", "Belarus": "Europe", "Belize": "North America",
    "Bolivia": "South America", "Brazil": "South America", "Canada": "North America",
    "Switzerland": "Europe", "Chile": "South America", "China": "Asia",
    "Côte d'Ivoire": "Africa", "Congo, Rep.": "Africa", "Colombia": "South America",
    "Cabo Verde": "Africa", "Costa Rica": "North America", "Cyprus": "Europe",
    "Czech Republic": "Europe", "Germany": "Europe", "Denmark": "Europe",
    "Dominican Republic": "North America", "Algeria": "Africa", "Ecuador": "South America",
    "Egypt, Arab Rep.": "Africa", "Spain": "Europe", "Estonia": "Europe",
    "Ethiopia": "Africa", "Finland": "Europe", "France": "Europe",
    "United Kingdom": "Europe", "Georgia": "Europe", "Ghana": "Africa",
    "Guinea": "Africa", "Greece": "Europe", "Grenada": "North America",
    "Hong Kong SAR, China": "Asia", "Honduras": "North America", "Croatia": "Europe",
    "Haiti": "North America", "Hungary": "Europe", "Indonesia": "Asia",
    "Ireland": "Europe", "Iceland": "Europe", "Israel": "Asia", "Italy": "Europe",
    "Jamaica": "North America", "Jordan": "Asia", "Japan": "Asia",
    "Kyrgyz Republic": "Asia", "Cambodia": "Asia", "Korea, Rep.": "Asia",
    "Lesotho": "Africa", "Lithuania": "Europe", "Luxembourg": "Europe",
    "Latvia": "Europe", "Macao SAR, China": "Asia", "Morocco": "Africa",
    "Maldives": "Asia", "Mexico": "North America", "North Macedonia": "Europe",
    "Malta": "Europe", "Mongolia": "Asia", "Mozambique": "Africa",
    "Mauritius": "Africa", "Malaysia": "Asia", "Namibia": "Africa", "Niger": "Africa",
    "Nigeria": "Africa", "Netherlands": "Europe", "Norway": "Europe",
    "Oman": "Asia", "Panama": "North America", "Philippines": "Asia",
    "Poland": "Europe", "Puerto Rico": "North America", "Portugal": "Europe",
    "Paraguay": "South America", "Romania": "Europe", "Russian Federation": "Europe",
    "Rwanda": "Africa", "Singapore": "Asia", "Sierra Leone": "Africa",
    "Serbia": "Europe", "Suriname": "South America", "Slovakia": "Europe",
    "Slovenia": "Europe", "Sweden": "Europe", "Togo": "Africa", "Thailand": "Asia",
    "Trinidad and Tobago": "North America", "Tunisia": "Africa", "Turkey": "Europe",
    "Taiwan, China": "Asia", "Ukraine": "Europe", "Uruguay": "South America",
    "United States": "North America", "Vietnam": "Asia", "Samoa": "Oceania",
    "Kosovo": "Europe", "South Africa": "Africa"
}

data['Continent'] = data['Country'].map(continent_mapping)

def calculate_continent_growth(year, prev_year):
    data_current_year = data.iloc[:, 5:].filter(regex=f'^{year}').dropna(how='all')
    data_prev_year = data.iloc[:, 5:].filter(regex=f'^{prev_year}').dropna(how='all')
    if data_prev_year.empty or data_current_year.empty:
        return None
    data_grouped_current = data.groupby('Continent')[data_current_year.columns].mean()
    data_grouped_prev = data.groupby('Continent')[data_prev_year.columns].mean()
    growth = data_grouped_current.subtract(data_grouped_prev, fill_value=0)
    return growth.mean(axis=1)

dashboard = lc.Dashboard(theme=lc.Themes.TurquoiseHexagon, rows=2, columns=3)


gauges = {}
row, col = 0, 0
for continent in ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']:
    gauges[continent] = dashboard.GaugeChart(row_index=row, column_index=col)
    gauges[continent].set_title(f"{continent}: Food Price Index Growth")
    gauges[continent].set_angle_interval(start=225, end=-45)
    gauges[continent].set_interval(start=-50, end=50) 
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
    continent_growth = calculate_continent_growth(year, prev_year)
    if continent_growth is not None:
        for continent, growth in continent_growth.items():
            if continent in gauges:
                gauges[continent].set_value(growth)
                gauges[continent].set_title(f"{continent}: Growth ({year})")
    print(f"Year: {year}, Growth: {continent_growth}")
    time.sleep(1) 
