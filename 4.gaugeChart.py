
# import pandas as pd
# import lightningchart as lc

# # Load the license key
# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the dataset
# file_path = 'Processed.xlsx'
# data = pd.read_excel(file_path, sheet_name='fcpi_m')

# # Define continent mapping
# continent_mapping = {
#     "Afghanistan": "Asia", "Albania": "Europe", "Austria": "Europe",
#     "Azerbaijan": "Asia", "Belgium": "Europe", "Bulgaria": "Europe",
#     "Bosnia and Herzegovina": "Europe", "Belarus": "Europe", "Belize": "North America",
#     "Bolivia": "South America", "Brazil": "South America", "Canada": "North America",
#     "Switzerland": "Europe", "Chile": "South America", "China": "Asia",
#     "Côte d'Ivoire": "Africa", "Congo, Rep.": "Africa", "Colombia": "South America",
#     "Cabo Verde": "Africa", "Costa Rica": "North America", "Cyprus": "Europe",
#     "Czech Republic": "Europe", "Germany": "Europe", "Denmark": "Europe",
#     "Dominican Republic": "North America", "Algeria": "Africa", "Ecuador": "South America",
#     "Egypt, Arab Rep.": "Africa", "Spain": "Europe", "Estonia": "Europe",
#     "Ethiopia": "Africa", "Finland": "Europe", "France": "Europe",
#     "United Kingdom": "Europe", "Georgia": "Europe", "Ghana": "Africa",
#     "Guinea": "Africa", "Greece": "Europe", "Grenada": "North America",
#     "Hong Kong SAR, China": "Asia", "Honduras": "North America", "Croatia": "Europe",
#     "Haiti": "North America", "Hungary": "Europe", "Indonesia": "Asia",
#     "Ireland": "Europe", "Iceland": "Europe", "Israel": "Asia", "Italy": "Europe",
#     "Jamaica": "North America", "Jordan": "Asia", "Japan": "Asia",
#     "Kyrgyz Republic": "Asia", "Cambodia": "Asia", "Korea, Rep.": "Asia",
#     "Lesotho": "Africa", "Lithuania": "Europe", "Luxembourg": "Europe",
#     "Latvia": "Europe", "Macao SAR, China": "Asia", "Morocco": "Africa",
#     "Maldives": "Asia", "Mexico": "North America", "North Macedonia": "Europe",
#     "Malta": "Europe", "Mongolia": "Asia", "Mozambique": "Africa",
#     "Mauritius": "Africa", "Malaysia": "Asia", "Namibia": "Africa", "Niger": "Africa",
#     "Nigeria": "Africa", "Netherlands": "Europe", "Norway": "Europe",
#     "Oman": "Asia", "Panama": "North America", "Philippines": "Asia",
#     "Poland": "Europe", "Puerto Rico": "North America", "Portugal": "Europe",
#     "Paraguay": "South America", "Romania": "Europe", "Russian Federation": "Europe",
#     "Rwanda": "Africa", "Singapore": "Asia", "Sierra Leone": "Africa",
#     "Serbia": "Europe", "Suriname": "South America", "Slovakia": "Europe",
#     "Slovenia": "Europe", "Sweden": "Europe", "Togo": "Africa", "Thailand": "Asia",
#     "Trinidad and Tobago": "North America", "Tunisia": "Africa", "Turkey": "Europe",
#     "Taiwan, China": "Asia", "Ukraine": "Europe", "Uruguay": "South America",
#     "United States": "North America", "Vietnam": "Asia", "Samoa": "Oceania",
#     "Kosovo": "Europe", "South Africa": "Africa"
# }
# # Add continent column to the dataset
# data['Continent'] = data['Country'].map(continent_mapping)

# # Filter data for the year 2023 and calculate mean for each continent
# data_filtered = data.iloc[:, 5:].filter(regex='^2023')
# data_grouped = data.groupby('Continent')[data_filtered.columns].mean()
# data_grouped['Average'] = data_grouped.mean(axis=1)

# # Prepare data for the Donut Chart
# chart_data = data_grouped['Average'].reset_index()
# chart_data.columns = ['Continent', 'Average']

# # Initialize the Donut Chart
# chart = lc.PieChart(
#     labels_inside_slices=True,
#     title='Donut Chart: Average Food Price Index by Continent (2023)',
#     theme=lc.Themes.TurquoiseHexagon,
# )

# # Add slices
# slices = []
# for i in range(len(chart_data)):
#     slices.append({
#         'name': chart_data.loc[i, 'Continent'],
#         'value': chart_data.loc[i, 'Average'],
#     })

# chart.set_label_formatter('NamePlusValue')
# chart.add_slices(slices)
# chart.set_inner_radius(50)

# # Add a legend
# legend = chart.add_legend(data=chart).set_title('Continents')

# # Open the chart
# chart.open()



# import pandas as pd
# import lightningchart as lc
# import time

# # Load the license key
# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load the dataset
# file_path = 'Processed.xlsx'
# data = pd.read_excel(file_path, sheet_name='fcpi_m')

# # Define continent mapping
# continent_mapping = {
#     "Afghanistan": "Asia", "Albania": "Europe", "Austria": "Europe",
#     "Azerbaijan": "Asia", "Belgium": "Europe", "Bulgaria": "Europe",
#     "Bosnia and Herzegovina": "Europe", "Belarus": "Europe", "Belize": "North America",
#     "Bolivia": "South America", "Brazil": "South America", "Canada": "North America",
#     "Switzerland": "Europe", "Chile": "South America", "China": "Asia",
#     "Côte d'Ivoire": "Africa", "Congo, Rep.": "Africa", "Colombia": "South America",
#     "Cabo Verde": "Africa", "Costa Rica": "North America", "Cyprus": "Europe",
#     "Czech Republic": "Europe", "Germany": "Europe", "Denmark": "Europe",
#     "Dominican Republic": "North America", "Algeria": "Africa", "Ecuador": "South America",
#     "Egypt, Arab Rep.": "Africa", "Spain": "Europe", "Estonia": "Europe",
#     "Ethiopia": "Africa", "Finland": "Europe", "France": "Europe",
#     "United Kingdom": "Europe", "Georgia": "Europe", "Ghana": "Africa",
#     "Guinea": "Africa", "Greece": "Europe", "Grenada": "North America",
#     "Hong Kong SAR, China": "Asia", "Honduras": "North America", "Croatia": "Europe",
#     "Haiti": "North America", "Hungary": "Europe", "Indonesia": "Asia",
#     "Ireland": "Europe", "Iceland": "Europe", "Israel": "Asia", "Italy": "Europe",
#     "Jamaica": "North America", "Jordan": "Asia", "Japan": "Asia",
#     "Kyrgyz Republic": "Asia", "Cambodia": "Asia", "Korea, Rep.": "Asia",
#     "Lesotho": "Africa", "Lithuania": "Europe", "Luxembourg": "Europe",
#     "Latvia": "Europe", "Macao SAR, China": "Asia", "Morocco": "Africa",
#     "Maldives": "Asia", "Mexico": "North America", "North Macedonia": "Europe",
#     "Malta": "Europe", "Mongolia": "Asia", "Mozambique": "Africa",
#     "Mauritius": "Africa", "Malaysia": "Asia", "Namibia": "Africa", "Niger": "Africa",
#     "Nigeria": "Africa", "Netherlands": "Europe", "Norway": "Europe",
#     "Oman": "Asia", "Panama": "North America", "Philippines": "Asia",
#     "Poland": "Europe", "Puerto Rico": "North America", "Portugal": "Europe",
#     "Paraguay": "South America", "Romania": "Europe", "Russian Federation": "Europe",
#     "Rwanda": "Africa", "Singapore": "Asia", "Sierra Leone": "Africa",
#     "Serbia": "Europe", "Suriname": "South America", "Slovakia": "Europe",
#     "Slovenia": "Europe", "Sweden": "Europe", "Togo": "Africa", "Thailand": "Asia",
#     "Trinidad and Tobago": "North America", "Tunisia": "Africa", "Turkey": "Europe",
#     "Taiwan, China": "Asia", "Ukraine": "Europe", "Uruguay": "South America",
#     "United States": "North America", "Vietnam": "Asia", "Samoa": "Oceania",
#     "Kosovo": "Europe", "South Africa": "Africa"
# }

# # Add continent column to the dataset
# data['Continent'] = data['Country'].map(continent_mapping)

# # Function to calculate the average food price index for each year
# def calculate_global_average(year):
#     data_filtered = data.iloc[:, 5:].filter(regex=f'^{year}')
#     data_grouped = data.groupby('Continent')[data_filtered.columns].mean()
#     data_grouped['Average'] = data_grouped.mean(axis=1)
#     global_average = data_grouped['Average'].mean()
#     return global_average

# # Initialize the Gauge Chart
# chart = lc.GaugeChart(
#     title="Real-Time Gauge Chart: Global Food Price Index",
#     theme=lc.Themes.Light
# )
# chart.set_angle_interval(start=225, end=-45)
# chart.set_interval(start=0, end=300)
# chart.set_bar_thickness(30)
# chart.set_value_indicator_thickness(10)
# chart.set_value_indicators([
#     {'start': 0, 'end': 100, 'color': lc.Color('green')},
#     {'start': 100, 'end': 200, 'color': lc.Color('yellow')},
#     {'start': 200, 'end': 300, 'color': lc.Color('red')}
# ])

# # Open the chart in live mode
# chart.open(live=True)

# # Simulate real-time updates
# for year in range(2020, 2024):
#     global_average = calculate_global_average(year)
#     chart.set_value(global_average)
#     chart.set_title(f"Global Average Food Price Index - Year {year}")
#     print(f"Year: {year}, Global Average: {global_average}")
#     time.sleep(2)  # Pause for 2 seconds to simulate real-time updates



import pandas as pd
import lightningchart as lc
import time

# Load the license key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Processed.xlsx'
data = pd.read_excel(file_path, sheet_name='fcpi_m')

# Define continent mapping
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

# Add continent column to the dataset
data['Continent'] = data['Country'].map(continent_mapping)

# Function to calculate the average food price index for each continent for a specific year
def calculate_continent_averages(year):
    data_filtered = data.iloc[:, 5:].filter(regex=f'^{year}')
    data_grouped = data.groupby('Continent')[data_filtered.columns].mean()
    averages = data_grouped.mean(axis=1)
    return averages

# Initialize the dashboard
dashboard = lc.Dashboard(theme=lc.Themes.TurquoiseHexagon, rows=2, columns=3)

# Add gauge charts for each continent
gauges = {}
row, col = 0, 0
for continent in ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']:
    gauges[continent] = dashboard.GaugeChart(row_index=row, column_index=col)
    gauges[continent].set_title(f"{continent}: Food Price Index")
    gauges[continent].set_angle_interval(start=225, end=-45)
    gauges[continent].set_interval(start=0, end=400)  
    gauges[continent].set_bar_thickness(20)
    gauges[continent].set_value_indicator_thickness(10)
    gauges[continent].set_value_label_font(30)  

    gauges[continent].set_value_indicators([
        {'start': 0, 'end': 100, 'color': lc.Color('green')},
        {'start': 100, 'end': 200, 'color': lc.Color('yellow')},
        {'start': 200, 'end': 400, 'color': lc.Color('red')}
    ])
    col += 1
    if col > 2: 
        col = 0
        row += 1

# Open the dashboard
dashboard.open(live=True)

# Simulate real-time updates for the last 10 years
for year in range(2013, 2024):
    continent_averages = calculate_continent_averages(year)
    for continent, avg in continent_averages.items():
        if continent in gauges:
            gauges[continent].set_value(avg)
            gauges[continent].set_title(f"{continent}: Food Price Index ({year})")
    print(f"Year: {year}, Averages: {continent_averages}")
    time.sleep(2)  # Pause for 2 seconds to simulate real-time updates




















# continent_mapping = {
#     "Asia": [
#         "Afghanistan", "Azerbaijan", "China", "Hong Kong SAR, China", "Indonesia", "Israel", 
#         "Japan", "Jordan", "Kyrgyz Republic", "Cambodia", "Korea, Rep.", "Macao SAR, China", 
#         "Maldives", "Mongolia", "Malaysia", "Oman", "Philippines", "Singapore", "Thailand", 
#         "Taiwan, China", "Vietnam"
#     ],
#     "Europe": [
#         "Albania", "Austria", "Belgium", "Bulgaria", "Bosnia and Herzegovina", "Belarus", 
#         "Switzerland", "Cyprus", "Czech Republic", "Germany", "Denmark", "Spain", "Estonia", 
#         "Finland", "France", "United Kingdom", "Georgia", "Greece", "Croatia", "Hungary", 
#         "Ireland", "Iceland", "Italy", "Lithuania", "Luxembourg", "Latvia", "North Macedonia", 
#         "Malta", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russian Federation", 
#         "Serbia", "Slovakia", "Slovenia", "Sweden", "Turkey", "Ukraine", "Kosovo"
#     ],
#     "North America": [
#         "Belize", "Canada", "Costa Rica", "Dominican Republic", "Grenada", "Honduras", "Haiti", 
#         "Jamaica", "Mexico", "Panama", "Puerto Rico", "Trinidad and Tobago", "United States"
#     ],
#     "South America": [
#         "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Suriname", "Uruguay"
#     ],
#     "Africa": [
#         "Côte d'Ivoire", "Congo, Rep.", "Cabo Verde", "Algeria", "Egypt, Arab Rep.", "Ethiopia", 
#         "Ghana", "Guinea", "Lesotho", "Morocco", "Mozambique", "Mauritius", "Namibia", "Niger", 
#         "Nigeria", "Rwanda", "Sierra Leone", "South Africa", "Togo", "Tunisia"
#     ],
#     "Oceania": ["Samoa"]
# }