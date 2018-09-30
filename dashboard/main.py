import os
import json
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from dashboard.scripts.panels.panel_return_histogram import panel_return_histogram
from dashboard.scripts.panels.panel_return_scatter import panel_return_scatter
from dashboard.scripts.utility import (
    create_random_quartile, check_data_format, create_test_data)

TEST_DATAPATH = 'dashboard/data/test_day.csv'
test_data = pd.read_csv(TEST_DATAPATH)
test_data['time'] = pd.to_datetime(test_data['time'], infer_datetime_format=True)
#test_data['test_quartile'] = create_random_quartile(len(test_data))

# print(test_data['RSI'].min())
# print(test_data['RSI'].max())

### Create tabs ###
tab1 = panel_return_histogram(test_data)
tab2 = panel_return_scatter(test_data)

### Put together tabs ###
tabs = Tabs(tabs=[tab1, tab2])

### Put the tabs for display ###
curdoc().add_root(tabs)



### END