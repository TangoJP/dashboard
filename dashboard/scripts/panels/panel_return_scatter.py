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
    widget_settings = widget_settings['panel_return_scatter']

settings_figure = {
    'plot_width': 600, 
    'plot_height': 600, 
    'title': 'Test Hitogram',
    'x_axis_label': 'Return (%)', 
    'y_axis_label': 'Proportion'
}

def panel_return_scatter(data):
    ### Create a figure ###
    p = figure(
        plot_width=settings_figure['plot_width'], 
        plot_height=settings_figure['plot_height'], 
        title=settings_figure['title'],
        toolbar_location="below"
    )
    p.background_fill_color = 'aliceblue'
    p.background_fill_alpha = 0.4

    p_hist_top = figure(plot_width=600, plot_height=150)
    p_hist_right = figure(plot_width=150, plot_height=600)

    def update_data():
        period = selector_period.value
        data['return'] = calculate_percent_return(data['close'], period)
        
        df = pd.DataFrame(
            {
                'x':data[selector_xmetric.value],
                'y':data[selector_ymetric.value],
                'return': data['return']
            }
        )

        return ColumnDataSource(df.dropna())

    def draw(source):
        # update_axes(p)
        

        mapper = LinearColorMapper(
            palette=all_palettes['RdBu'][len(source.data)], 
            low=-2.5,   #np.nanmin(source.data['return']), 
            high=2.5    #np.nanmax(source.data['return'])
        )

        p.circle(
            source=source, 
            x='x', 
            y='y',
            color={'field': 'return', 'transform': mapper},
            fill_alpha=0.3,
            line_alpha=0.4,
            size=8,
            hover_fill_alpha=1.0
        )
        color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
        p.add_layout(color_bar, 'right')


        return column(p_hist_top, row(p, p_hist_right))

    def update():
        source_updated = update_data()
        source.data = source_updated.data

        p.xaxis.axis_label = selector_xmetric.value
        p.yaxis.axis_label = selector_ymetric.value

        bins = 40
        x_hist, x_edges = np.histogram(source.data['x'], bins=bins)
        y_hist, y_edges = np.histogram(source.data['y'], bins=bins)
        
        p_hist_top.quad(
            bottom=0, top=x_hist, 
            left=x_edges[:-1], right=x_edges[1:]
        )
        
        p_hist_right.quad(
            bottom=y_edges[1:], top=y_edges[:-1], 
            left=0, right=y_hist
        )

    selector_period = create_widget(widget_settings['return_period'])
    selector_xmetric = create_widget(widget_settings['xmetric'])
    selector_ymetric = create_widget(widget_settings['ymetric'])

    selector_period.on_change('value', lambda attr, old, new: update())
    selector_xmetric.on_change('value', lambda attr, old, new: update())
    selector_ymetric.on_change('value', lambda attr, old, new: update())

    source = update_data()
    p_column = draw(source)

    ### Setting up the laytou ###
    # Widgets
    controlers = WidgetBox(
        selector_period,
        selector_xmetric,
        selector_ymetric,
        width=350
    )

    # Layout
    layout = row(controlers, p_column)
    panel = Panel(child=layout, title='Return Analysis')

    return panel