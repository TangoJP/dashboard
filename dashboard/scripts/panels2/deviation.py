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
from dashboard.scripts.utility import (
    Slice, calculate_percent_return, check_data_format)
from dashboard.scripts.utility2 import (
    add_return, add_SMA, add_SMA_deviation)

with open('dashboard/scripts/json/widgets2.json') as json_widgets:
    widget_settings = json.load(json_widgets)
    widget_settings = widget_settings['deviation']

# Figure attributes. TO BE SENT TO A JSON
settings_figure = {
    'plot_width': 450, 
    'plot_height': 500, 
    'title': 'Test Hitogram',
    'x_axis_label': 'Deviation', 
    'y_axis_label': 'Return'
}

def tab_deviation(data):
    p = figure(
        plot_width=settings_figure['plot_width'], 
        plot_height=settings_figure['plot_height'], 
        title=settings_figure['title'],
        toolbar_location="right",
        toolbar_sticky=False,
        x_axis_label=settings_figure['x_axis_label'],
        y_axis_label=settings_figure['y_axis_label']
    )
    p.background_fill_color = 'aliceblue'
    p.background_fill_alpha = 0.4

    ### Initial ColumnDataSource
    initial_return_period = 1
    initial_sma_period = 5
    initial_percent_or_not = True
    add_return(data, initial_return_period, percent=initial_percent_or_not)
    add_SMA_deviation(data, initial_sma_period, percent=initial_percent_or_not)

    source = ColumnDataSource(
        {
            'x': data['SMA_deviation'],
            'y': data['return'],
        }
    )

    p.circle(
        source=source, 
        x='x', 
        y='y',
        #color={'field': 'return', 'transform': mapper},
        fill_alpha=0.2,
        line_alpha=0.4,
        size=3
    )

    selector_return_period = create_widget(widget_settings['return_period'])
    selector_sma_period = create_widget(widget_settings['sma_period'])
    #selector_percent = create_widget(widget_settings['percent'])

    def update():
        return_period = selector_return_period.value
        sma_period = selector_sma_period.value
        #percent_or_not = selector_percent.labels[selector_percent.active]
        add_return(data, return_period, percent=True)
        add_SMA(data, sma_period)
        add_SMA_deviation(data, sma_period, percent=True)

        source.data = {
            'x': data['SMA_deviation'],
            'y': data['return'],
        }

    selector_return_period.on_change('value', lambda attr, old, new: update())
    selector_sma_period.on_change('value', lambda attr, old, new: update())
    #selector_percent.on_change('active', lambda attr, old, new: update())

    ### Layout ###
    controlers = WidgetBox(
        selector_return_period,
        selector_sma_period,
        width=350
    )
    layout = row(controlers, p)
    panel = Panel(child=layout, title='Return Analysis')

    return panel

###
