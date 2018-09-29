import unittest
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from dashboard.scripts.plot import plot_histogram

import matplotlib.pyplot as plt

class TestHistogram(unittest.TestCase):

    def setUp(self):
        DATAPATH = 'dashboard/data/fx/EURJPY/EURJPY_2002-201802_day.csv'
        self.df = pd.read_csv(DATAPATH)
        self.df['time'] = pd.to_datetime(
            self.df['time'], infer_datetime_format=True)
        
        self.p = figure(
            title='Test Histogram',
            plot_height=500,
            plot_width=500
        )

    # def test_data(self):
    #     print(self.df.columns)
    #     plt.plot(self.df['time'], self.df['close'])
    #     plt.show()

    def test_plot_histogram(self):
        p = plot_histogram(self.p, self.df['close'])
        show(p)

if __name__ == '__main__':
    unittest.main()