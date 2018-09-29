import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource

def plot_histogram(p, source, bins=20):
    if isinstance(source, ColumnDataSource):
        series = source.data['y']
    if isinstance(source, pd.Series):
        series = source
    hist, edges = np.histogram(series, bins=bins)

    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:])

    return p