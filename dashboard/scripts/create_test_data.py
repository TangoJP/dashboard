import pandas as pd
import numpy as np
from dashboard.scripts.utility import create_test_data



TEST_DATAPATH = 'dashboard/data/fx/EURJPY/EURJPY_2002-201802_day.csv'
test_data = pd.read_csv(TEST_DATAPATH)
test_data['time'] = pd.to_datetime(test_data['time'], infer_datetime_format=True)
test_data = create_test_data(test_data)
test_data.to_csv('dashboard/data/test_day.csv', index=False)


TEST_DATAPATH = 'dashboard/data/fx/EURJPY/EURJPY_2002-201802_hour.csv'
test_data = pd.read_csv(TEST_DATAPATH)
test_data['time'] = pd.to_datetime(test_data['time'], infer_datetime_format=True)
test_data = create_test_data(test_data)
test_data.to_csv('dashboard/data/test_hour.csv', index=False)