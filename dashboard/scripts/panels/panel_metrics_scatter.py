import json
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column, row, WidgetBox
from bokeh.models import (
    ColumnDataSource, Panel, HoverTool, LinearColorMapper, ColorBar)
from bokeh.palettes import all_palettes, Viridis
from dashboard.scripts.widgets import create_widget
from dashboard.scripts.plot import plot_histogram
from dashboard.scripts.utility import Slice, calculate_percent_return

with open('dashboard/scripts/json/widgets.json') as json_widgets:
    widget_settings = json.load(json_widgets)
    widget_settings = widget_settings['panel_metrics_scatter']

settings_figure = {
    'plot_width': 450, 
    'plot_height': 500, 
    'title': 'Test Hitogram',
    'x_axis_label': 'Return (%)', 
    'y_axis_label': 'Proportion'
}

def panel_metrics_scatter(data):

    ### Create a figure ###
    p = figure(
        plot_width=settings_figure['plot_width'], 
        plot_height=settings_figure['plot_height'], 
        title=settings_figure['title'],
        toolbar_location="below",
        toolbar_sticky=False
    )
    p.background_fill_color = 'aliceblue'
    p.background_fill_alpha = 0.4

    p_hist_top = figure(
        toolbar_location=None,
        plot_width=settings_figure['plot_width'], 
        plot_height=150
    )
    p_hist_right = figure(
        toolbar_location=None,
        plot_width=150, 
        plot_height=settings_figure['plot_height'])

    source_main = ColumnDataSource(
        {
            'x': data['MACD'],
            'y': data['MACD'],
            'return': calculate_percent_return(data['close'], 1)
        }
    )

    x_hist, x_edges = np.histogram(data['SMA_Deviation_Sigma'].dropna(), bins=100)
    y_hist, y_edges = np.histogram(data['MACD_signal'].dropna(), bins=100)
    source_hist = ColumnDataSource(
        {
            'x_hist': x_hist,
            'y_hist': y_hist,
            'x_edges': x_edges[:-1],
            'y_edges': y_edges[1:]
        }
    )

    mapper = LinearColorMapper(
            palette=all_palettes['RdBu'][len(source_main.data)], 
            low=-2.5,   #np.nanmin(source.data['return']), 
            high=2.5    #np.nanmax(source.data['return'])
    )

    p.circle(
        source=source_main, 
        x='x', 
        y='y',
        color={'field': 'return', 'transform': mapper},
        fill_alpha=0.2,
        line_alpha=0.4,
        size=3,
        hover_fill_alpha=1.0
    )
    p_hist_top.quad(
        source=source_hist,
        bottom=0, top='x_hist', 
        left='x_edges', right='x_edges'
    )
    p_hist_right.quad(
        source=source_hist,
        bottom='y_edges', top='y_edges', 
        left=0, right='y_hist'
    )

    p_column = column(p_hist_top, row(p, p_hist_right))

    def update():
        period = selector_period.value
        data_return = calculate_percent_return(data['close'], period)
        bins = selector_bins.value

        xdata = data[selector_xmetric.value]
        ydata = data[selector_ymetric.value]
        
        source_main.data = {
                'x':xdata,
                'y':ydata,
                'return': data_return
        }

        x_hist, x_edges = np.histogram(xdata.dropna(), bins=bins, density=True)
        y_hist, y_edges = np.histogram(ydata.dropna(), bins=bins, density=True)
        source_hist.data = {
            'x_hist': x_hist,
            'y_hist': y_hist,
            'x_edges': x_edges[:-1],
            'y_edges': y_edges[1:]
        }
        return

    selector_period = create_widget(widget_settings['return_period'])
    selector_xmetric = create_widget(widget_settings['xmetric'])
    selector_ymetric = create_widget(widget_settings['ymetric'])
    selector_bins = create_widget(widget_settings['bins'])

    selector_period.on_change('value', lambda attr, old, new: update())
    selector_xmetric.on_change('value', lambda attr, old, new: update())
    selector_ymetric.on_change('value', lambda attr, old, new: update())
    selector_bins.on_change('value', lambda attr, old, new: update())

    ### Setting up the laytou ###
    # Widgets
    controlers = WidgetBox(
        selector_period,
        selector_xmetric,
        selector_ymetric,
        selector_bins,
        width=350
    )

    # Layout
    layout = row(controlers, p_column)
    panel = Panel(child=layout, title='Return Analysis')

    return panel