import pandas as pd

# 读取CSV文件，兼容常见编码
def load_shipping_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, encoding='gbk')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='ansi')
    
    # 标准列名
    df.columns = ['Country', 'Transit Time', 'Weight (KG)', 'Shipping Rate (RMB/KG)', 'Fuel Surcharge (RMB/order)']
    
    # 处理重量区间
    df[['Min Weight', 'Max Weight']] = df['Weight (KG)'].str.extract(r'([\d.]+)\D+([\d.]+)')
    df['Min Weight'] = pd.to_numeric(df['Min Weight'])
    df['Max Weight'] = pd.to_numeric(df['Max Weight'])
    
    return df

# 运费计算函数
def calculate_shipping(country, weight, df):
    country_data = df[df['Country'].str.lower() == country.lower()]
    
    if country_data.empty:
        return None, None, None, f"Error: No shipping data found for country '{country}'"
    
    applicable_row = country_data[
        (country_data['Min Weight'] <= weight) & 
        (country_data['Max Weight'] >= weight)
    ]
    
    if applicable_row.empty:
        # 尝试最大重量费率
        applicable_row = country_data[country_data['Max Weight'] >= weight].head(1)
        if applicable_row.empty:
            applicable_row = country_data[country_data['Max Weight'] == country_data['Max Weight'].max()]
            if applicable_row.empty:
                return None, None, None, f"Error: No shipping data found for weight {weight}kg"
    
    shipping_time = applicable_row['Transit Time'].values[0]
    unit_price = applicable_row['Shipping Rate (RMB/KG)'].values[0]
    fuel_surcharge = applicable_row['Fuel Surcharge (RMB/order)'].values[0]
    total_cost = weight * unit_price + fuel_surcharge

    return shipping_time, unit_price, fuel_surcharge, total_cost

# 命令行主程序
def main():
    print("International Shipping Fee Calculator")
    print("=" * 40)
    
    try:
        df = load_shipping_data('yuntuPriceEn.csv')
    except FileNotFoundError:
        print("Error: File 'yuntuPriceEn.csv' not found in the directory.")
        return

    available_countries = df['Country'].unique()
    print("\nAvailable Countries:")
    print(", ".join(available_countries))
    
    while True:
        print("\n" + "=" * 40)
        country = input("Enter destination country (or 'q' to quit): ").strip()
        if country.lower() == 'q':
            break
        
        if country not in available_countries:
            print(f"Error: Country '{country}' is not in the list.")
            continue
        
        try:
            weight = float(input("Enter package weight (kg): ").strip())
            if weight <= 0:
                print("Error: Weight must be greater than 0.")
                continue
        except ValueError:
            print("Error: Invalid weight input.")
            continue
        
        shipping_time, unit_price, fuel_surcharge, result = calculate_shipping(country, weight, df)

        if isinstance(result, str):  # Error
            print(result)
        else:
            print("\nShipping Details:")
            print(f"Country: {country}")
            print(f"Weight: {weight} kg")
            print(f"Estimated Transit Time: {shipping_time}")
            print(f"Rate per KG: {unit_price} RMB")
            print(f"Fuel Surcharge: {fuel_surcharge} RMB")
            print(f"Total Cost: {result:.2f} RMB")

if __name__ == "__main__":
    main()
