import lightningchart as lc
import pandas as pd


with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)


file_path = 'Processed.xlsx'

selected_country = "Ukraine"
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
    title=f"Food Price Index for {selected_country} (2018-2023)"
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