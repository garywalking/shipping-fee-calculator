import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from shippingFee_calculator import calculate_shipping, load_shipping_data

# 加载测试数据
df = load_shipping_data('yuntuPriceEn.csv')

def test_calculate_shipping_us_valid():
    country = 'US'
    weight = 2.0
    transit_time, unit_price, fuel_surcharge, total = calculate_shipping(country, weight, df)

    assert isinstance(transit_time, str)
    assert isinstance(unit_price, (int, float, np.integer, np.floating))
    assert isinstance(fuel_surcharge, (int, float, np.integer, np.floating))
    assert isinstance(total, (int, float, np.integer, np.floating))
    assert total > 0
