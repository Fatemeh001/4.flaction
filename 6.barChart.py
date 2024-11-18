import lightningchart as lc
import pandas as pd


with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)


file_path = 'Processed.xlsx'
fcpi_data = pd.read_excel(file_path, sheet_name='fcpi_m')
ecpi_data = pd.read_excel(file_path, sheet_name='ecpi_m')


country = "Turkey" 


if country in fcpi_data['Country'].values and country in ecpi_data['Country'].values:
    
    fcpi_country_data = fcpi_data[fcpi_data['Country'] == country]
    ecpi_country_data = ecpi_data[ecpi_data['Country'] == country]

    
    def calculate_yearly_averages(data, start_year=2000, end_year=2023):
        yearly_averages = {}
        for year in range(start_year, end_year + 1):
            
            year_columns = [col for col in data.columns if isinstance(col, (int, str)) and str(col).startswith(str(year))]
            if year_columns:
                yearly_averages[str(year)] = data[year_columns].mean(axis=1).values[0]
        return yearly_averages

   
    fcpi_yearly_avg = calculate_yearly_averages(fcpi_country_data)
    ecpi_yearly_avg = calculate_yearly_averages(ecpi_country_data)

    
    valid_years = sorted(fcpi_yearly_avg.keys() & ecpi_yearly_avg.keys())
    if valid_years:
        data = [
            {'subCategory': 'FCPI', 'values': [fcpi_yearly_avg[year] for year in valid_years]},
            {'subCategory': 'ECPI', 'values': [ecpi_yearly_avg[year] for year in valid_years]},
        ]

  
        chart = lc.BarChart(
            vertical=True,
            theme=lc.Themes.Light,
            title=f'Yearly Comparison of FCPI and ECPI for {country} (2018-2023)'
        )

       
        chart.set_data_grouped(
            
            valid_years, 
            data
        )

        
        chart.set_label_rotation(45)  
        chart.set_value_label_font_size(14)  

        
        chart.set_bars_margin(0.2)  

        
        legend = chart.add_legend().add(chart)
     

        
        chart.open()
    else:
        print("No valid years available for the years 2018-2023 for Turkey.")
else:
    print(f"{country} does not exist in one or both datasets.")
