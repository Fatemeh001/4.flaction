
import pandas as pd
import lightningchart as lc

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

# Filter data for the year 2023 and calculate mean for each continent
data_filtered = data.iloc[:, 5:].filter(regex='^2023')
data_grouped = data.groupby('Continent')[data_filtered.columns].mean()
data_grouped['Average'] = data_grouped.mean(axis=1)

# Prepare data for the Donut Chart
chart_data = data_grouped['Average'].reset_index()
chart_data.columns = ['Continent', 'Average']

# Initialize the Donut Chart
chart = lc.PieChart(
    labels_inside_slices=True,
    title='Donut Chart: Average Food Price Index by Continent (2023)',
    theme=lc.Themes.TurquoiseHexagon,
)

# Add slices
slices = []
for i in range(len(chart_data)):
    slices.append({
        'name': chart_data.loc[i, 'Continent'],
        'value': chart_data.loc[i, 'Average'],
    })

chart.set_label_formatter('NamePlusValue')
chart.add_slices(slices)
chart.set_inner_radius(50)

# Add a legend
legend = chart.add_legend(data=chart).set_title('Continents')

# Open the chart
chart.open()
