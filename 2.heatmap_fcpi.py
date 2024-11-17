import pandas as pd
import numpy as np
import lightningchart as lc

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Processed.xlsx'

selected_country = "Albania"
data = pd.read_excel(file_path, sheet_name='fcpi_m')
selected_country_data = data[data['Country'] == selected_country].iloc[:, 5:]

data_selected_years = selected_country_data.filter(regex='^2000|^2001|^2002|^2003|^2004|^2005|^2006|^2007|^2008|^2009|^2010|^2011|^2012|^2013|^2014|^2015|^2016|^2017|^2018|^2019|^2020|^2021|^2022|^2023')
data_selected_years.columns = [str(col) for col in data_selected_years.columns]

data_selected_years_t = data_selected_years.T
data_selected_years_t.columns = ['Index Value']
data_selected_years_t['Year'] = data_selected_years_t.index.str[:4].astype(int)
data_selected_years_t['Month'] = data_selected_years_t.index.str[4:6].astype(int)

heatmap_data = data_selected_years_t.pivot(index="Month", columns="Year", values="Index Value").fillna(0).values

years = data_selected_years_t['Year'].unique()
years_ms = [int(pd.Timestamp(year=year, month=1, day=1).timestamp() * 1000) for year in years]

chart = lc.ChartXY(
    title=f"Food Price Index Heatmap for {selected_country} (2000-2023)",
    theme=lc.Themes.Dark
)

grid_size_x, grid_size_y = heatmap_data.shape
heatmap_series = chart.add_heatmap_grid_series(
    columns=grid_size_x,
    rows=grid_size_y
)

heatmap_series.set_start(x=years_ms[0], y=1)
heatmap_series.set_end(x=years_ms[-1], y=12)  
heatmap_series.set_step(x=(years_ms[-1] - years_ms[0]) / grid_size_x, y=1)

heatmap_series.set_intensity_interpolation(True)
heatmap_series.invalidate_intensity_values(heatmap_data.tolist())

heatmap_series.hide_wireframe()

heatmap_series.set_palette_coloring([
    {"value": np.min(heatmap_data), "color": lc.Color(0, 0, 255)}, 
    {"value": np.max(heatmap_data), "color": lc.Color(255, 0, 0)}   
])

chart.get_default_x_axis().set_title('Year')
chart.get_default_y_axis().set_title('Month')

x_axis = chart.get_default_x_axis()
x_axis.set_tick_strategy('DateTime', utc=True)

y_axis = chart.get_default_y_axis()
y_axis.set_interval(1, 12, 1)  

chart.add_legend(data=heatmap_series).set_title('Index Intensity')


chart.open()



