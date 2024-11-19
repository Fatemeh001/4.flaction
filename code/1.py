import pandas as pd
from pycountry_convert import country_name_to_country_alpha2, country_alpha2_to_continent_code
import lightningchart as lc

# خواندن لایسنس
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# تابع برای تعیین قاره‌ها
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

# خواندن داده‌های شاخص‌ها
file_path = 'dataset/Processed.xlsx'
fcpi_data = pd.read_excel(file_path, sheet_name='fcpi_m')
ecpi_data = pd.read_excel(file_path, sheet_name='ecpi_m')

# افزودن قاره‌ها به داده‌ها
fcpi_data['Continent'] = fcpi_data['Country'].apply(get_continent)
ecpi_data['Continent'] = ecpi_data['Country'].apply(get_continent)

# تبدیل داده‌ها از حالت گسترده به طولی
fcpi_data = fcpi_data.melt(id_vars=['Country', 'Continent'], var_name='Date', value_name='FCPI')
ecpi_data = ecpi_data.melt(id_vars=['Country', 'Continent'], var_name='Date', value_name='ECPI')

# فیلتر کردن مقادیر نامعتبر در ستون 'Date'
fcpi_data = fcpi_data[fcpi_data['Date'].str.isdigit() & (fcpi_data['Date'].str.len() == 6)]
ecpi_data = ecpi_data[ecpi_data['Date'].str.isdigit() & (ecpi_data['Date'].str.len() == 6)]

# استخراج سال از ستون Date
fcpi_data['Year'] = fcpi_data['Date'].astype(str).str[:4].astype(int)
ecpi_data['Year'] = ecpi_data['Date'].astype(str).str[:4].astype(int)

# حذف داده‌های با مقدار NaN
fcpi_data = fcpi_data.dropna(subset=['FCPI'])
ecpi_data = ecpi_data.dropna(subset=['ECPI'])

# محاسبه میانگین سالانه برای هر قاره
fcpi_grouped = fcpi_data.groupby(['Continent', 'Year'])['FCPI'].mean().reset_index()
ecpi_grouped = ecpi_data.groupby(['Continent', 'Year'])['ECPI'].mean().reset_index()

# ادغام داده‌های FCPI و ECPI
merged_data = pd.merge(fcpi_grouped, ecpi_grouped, on=['Continent', 'Year'], how='inner')

# دیباگ: بررسی داده‌های پردازش شده
print(merged_data.head())

# ایجاد نمودار
chart = lc.Chart3D(
    theme=lc.Themes.Light,
    title='3D Line Chart: Food and Energy Prices over Time'
)
chart.get_default_x_axis().set_title('Food Price Index (FCPI)')
chart.get_default_y_axis().set_title('Energy Price Index (ECPI)')
chart.get_default_z_axis().set_title('Year')

# افزودن سری‌ها برای هر قاره
continents = merged_data['Continent'].unique()
for continent in continents:
    continent_data = merged_data[merged_data['Continent'] == continent]
    if continent_data.empty:
        print(f"No data for continent: {continent}")
        continue
    # دیباگ: بررسی داده‌های هر قاره
    print(f"Data for {continent}:")
    print(continent_data)
    data_points = [{'x': row['FCPI'], 'y': row['ECPI'], 'z': row['Year']} for idx, row in continent_data.iterrows()]
    series = chart.add_line_series()
    series.set_line_thickness(2)
    series.set_data(data_points)
    series.set_name(continent)

# نمایش نمودار
chart.open()
