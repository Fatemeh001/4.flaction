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

# Select a specific country
country = "Turkey"  # Change this to your desired country

# Check if the country exists in both datasets
if country in fcpi_data['Country'].values and country in ecpi_data['Country'].values:
    # Extract data for the last 5 years (2018–2023)
    years = [str(year) for year in range(2018, 2024)]
    
    # Calculate yearly averages for FCPI and ECPI
    fcpi_yearly_avg = (
        fcpi_data[fcpi_data['Country'] == country]
        .filter(regex='^' + '|^'.join(years))
        .mean()
    )
    ecpi_yearly_avg = (
        ecpi_data[ecpi_data['Country'] == country]
        .filter(regex='^' + '|^'.join(years))
        .mean()
    )
    
    # Prepare data for Grouped Bar Chart
    data = [
        {'subCategory': 'FCPI', 'values': fcpi_yearly_avg.values.tolist()},
        {'subCategory': 'ECPI', 'values': ecpi_yearly_avg.values.tolist()},
    ]

    # Create the Grouped Bar Chart
    chart = lc.BarChart(
        vertical=True,
        theme=lc.Themes.TurquoiseHexagon,
        title=f'Yearly Comparison of FCPI and ECPI for {country} (2018-2023)'
    )

    # Set data for Grouped Bar Chart
    chart.set_data_grouped(
        years,  # Years as main categories
        data
    )

    # Customize individual bar colors
    chart.set_bar_color('FCPI', lc.Color('#1f77b4'))  # Blue
    chart.set_bar_color('ECPI', lc.Color('#ff7f0e'))  # Orange

    # Customize label rotation and font size
    chart.set_label_rotation(45)  # Rotate year labels for better visibility
    chart.set_value_label_font_size(14)  # Increase value label font size

    # Add bar margins for better spacing
    chart.set_bars_margin(0.2)  # Add spacing between bars

    # Add a legend
    legend = chart.add_legend()
    legend.add(chart)

    # Open the chart
    chart.open()

