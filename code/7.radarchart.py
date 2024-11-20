
import lightningchart as lc
import pandas as pd


with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)


file_path = 'dataset/Processed.xlsx'
fcpi_data = pd.read_excel(file_path, sheet_name='fcpi_m')
ecpi_data = pd.read_excel(file_path, sheet_name='ecpi_m')
def_a_data = pd.read_excel(file_path, sheet_name='def_a')


country = "Turkey"

if all(country in data['Country'].values for data in [fcpi_data, ecpi_data, def_a_data]):
    fcpi_country_data = fcpi_data[fcpi_data['Country'] == country]
    ecpi_country_data = ecpi_data[ecpi_data['Country'] == country]
    def_a_country_data = def_a_data[def_a_data['Country'] == country]

    years = [str(year) for year in range(2015, 2024)]

    def calculate_yearly_averages(data, years):
        yearly_averages = []
        for year in years:
            year_columns = [col for col in data.columns if isinstance(col, (int, str)) and str(col).startswith(year)]
            if year_columns:
                yearly_averages.append(data[year_columns].mean(axis=1).values[0])
            else:
                yearly_averages.append(None)
        return yearly_averages

    fcpi_yearly_avg = calculate_yearly_averages(fcpi_country_data, years)
    ecpi_yearly_avg = calculate_yearly_averages(ecpi_country_data, years)

    def_a_values = [
        def_a_country_data[year].values[0] if year in def_a_country_data.columns else None
        for year in map(int, years)
    ]

    chart = lc.SpiderChart(
        theme=lc.Themes.TurquoiseHexagon,
        title=f'Radar Chart: FCPI, ECPI, and DEF_A for {country} (2015-2023)'
    )

    for year in years:
        chart.add_axis(tag=year)

    fcpi_series = chart.add_series()
    fcpi_series.add_points([
        {'axis': year, 'value': value}
        for year, value in zip(years, fcpi_yearly_avg)
        if value is not None
    ])
    fcpi_series.set_line_color(lc.Color(31, 119, 180))  # Blue
    fcpi_series.set_fill_color(lc.Color(31, 119, 180, 100))  # Blue with transparency
    fcpi_series.set_name('FCPI')

    ecpi_series = chart.add_series()
    ecpi_series.add_points([
        {'axis': year, 'value': value}
        for year, value in zip(years, ecpi_yearly_avg)
        if value is not None
    ])
    ecpi_series.set_line_color(lc.Color(255, 127, 14))  # Orange
    ecpi_series.set_fill_color(lc.Color(255, 127, 14, 100))  # Orange with transparency
    ecpi_series.set_name('ECPI')

    def_a_series = chart.add_series()
    def_a_series.add_points([
        {'axis': year, 'value': value}
        for year, value in zip(years, def_a_values)
        if value is not None
    ])
    def_a_series.set_line_color(lc.Color(44, 160, 44))  # Green
    def_a_series.set_fill_color(lc.Color(44, 160, 44, 100))  # Green with transparency
    def_a_series.set_name('DEF_A')

    legend = chart.add_legend()
    legend.add(fcpi_series).add(ecpi_series).add(def_a_series)

    chart.open()
else:
    print(f"Country '{country}' does not exist in all datasets.")
