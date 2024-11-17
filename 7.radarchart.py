import lightningchart as lc
import pandas as pd

# Load the license key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load datasets
file_path = 'Processed.xlsx'
fcpi_data = pd.read_excel(file_path, sheet_name='fcpi_m')
ecpi_data = pd.read_excel(file_path, sheet_name='ecpi_m')
def_a_data = pd.read_excel(file_path, sheet_name='def_a')

# Select a specific country
country = "Turkey"  # Change this to your desired country

# Check if the country exists in all datasets
if all(country in data['Country'].values for data in [fcpi_data, ecpi_data, def_a_data]):
    # Extract data for the last 5 years (2018–2023)
    years = [str(year) for year in range(2018, 2024)]

    # Calculate yearly averages for FCPI, ECPI, and DEF_A
    fcpi_yearly_avg = (
        fcpi_data[fcpi_data['Country'] == country]
        .filter(regex='^' + '|^'.join(years))
        .mean()
        .values
    )
    ecpi_yearly_avg = (
        ecpi_data[ecpi_data['Country'] == country]
        .filter(regex='^' + '|^'.join(years))
        .mean()
        .values
    )
    def_a_yearly_avg = (
        def_a_data[def_a_data['Country'] == country]
        .filter(regex='^' + '|^'.join(years))
        .mean()
        .values
    )

    # Prepare data for Radar Chart
    chart = lc.SpiderChart(
        theme=lc.Themes.TurquoiseHexagon,
        title=f'Radar Chart: FCPI, ECPI, DEF_A for {country} (2018–2023)'
    )

    # Add axes (years as labels)
    for year in years:
        chart.add_axis(tag=year)

    # Add FCPI series
    fcpi_series = chart.add_series()
    fcpi_series.add_points([
        {'axis': year, 'value': value}
        for year, value in zip(years, fcpi_yearly_avg)
    ])
    fcpi_series.set_line_color(lc.Color(31, 119, 180))  # Blue
    fcpi_series.set_fill_color(lc.Color(31, 119, 180, 100))  # Blue with transparency
    fcpi_series.set_name('FCPI')

    # Add ECPI series
    ecpi_series = chart.add_series()
    ecpi_series.add_points([
        {'axis': year, 'value': value}
        for year, value in zip(years, ecpi_yearly_avg)
    ])
    ecpi_series.set_line_color(lc.Color(255, 127, 14))  # Orange
    ecpi_series.set_fill_color(lc.Color(255, 127, 14, 100))  # Orange with transparency
    ecpi_series.set_name('ECPI')

    # Add DEF_A series
    def_a_series = chart.add_series()
    def_a_series.add_points([
        {'axis': year, 'value': value}
        for year, value in zip(years, def_a_yearly_avg)
    ])
    def_a_series.set_line_color(lc.Color(44, 160, 44))  # Green
    def_a_series.set_fill_color(lc.Color(44, 160, 44, 100))  # Green with transparency
    def_a_series.set_name('DEF_A')

    # Add a legend
    legend = chart.add_legend()
    legend.add(fcpi_series).add(ecpi_series).add(def_a_series)  # Ensure all series are added to the legend

    # Open the chart
    chart.open()
else:
    print(f"Country '{country}' does not exist in all datasets.")
