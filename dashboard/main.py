import os
import json
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from dashboard.scripts.panels.panel_return import panel_return
from dashboard.scripts.utility import create_random_quartile

TEST_DATAPATH = 'dashboard/data/fx/EURJPY/EURJPY_2002-201802_hour.csv'
test_data = pd.read_csv(TEST_DATAPATH)
test_data['time'] = pd.to_datetime(test_data['time'], infer_datetime_format=True)
test_data['test_quartile'] = create_random_quartile(len(test_data))


### Create tabs ###
tab1 = panel_return(test_data)

### Put together tabs ###
tabs = Tabs(tabs=[tab1])

### Put the tabs for display ###
curdoc().add_root(tabs)