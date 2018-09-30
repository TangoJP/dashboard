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

    p_hist_top = figure(plot_width=600, plot_height=100)
    p_hist_right = figure(plot_width=100, plot_height=600)

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
            low=-2.5,#np.nanmin(source.data['return']), 
            high=2.5#np.nanmax(source.data['return'])
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

        #hover = HoverTool(tooltips=[('Quantile', '@name')],mode='vline')

        color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
        
        #p.add_tools(hover)
        p.add_layout(color_bar, 'right')

        return column(p_hist_top, row(p, p_hist_right))

    def update():
        source_updated = update_data()
        source.data = source_updated.data

        p.xaxis.axis_label = selector_xmetric.value
        p.yaxis.axis_label = selector_ymetric.value
        
    # def update_axes(p):
    #     choice_xrange = selector_xrange.value
    #     p.x_range.start = choice_xrange[0]
    #     p.x_range.end = choice_xrange[1]

    #     choice_yrange = selector_yrange.value
    #     p.y_range.start = choice_yrange[0]
    #     p.y_range.end = choice_yrange[1]

    selector_period = create_widget(widget_settings['return_period'])
    selector_xmetric = create_widget(widget_settings['xmetric'])
    selector_ymetric = create_widget(widget_settings['ymetric'])
    selector_xrange = create_widget(widget_settings['xrange'])
    selector_yrange = create_widget(widget_settings['yrange'])

    selector_period.on_change('value', lambda attr, old, new: update())
    selector_xmetric.on_change('value', lambda attr, old, new: update())
    selector_ymetric.on_change('value', lambda attr, old, new: update())
    #selector_xrange.on_change('value', lambda attr, old, new: update_axes(p))
    #selector_yrange.on_change('value', lambda attr, old, new: update_axes(p))

    source = update_data()
    p_column = draw(source)

    ### Setting up the laytou ###
    # Widgets
    controlers = WidgetBox(
        selector_period,
        selector_xmetric,
        selector_ymetric,
        selector_xrange,
        selector_yrange,
        width=350
    )

    # Layout
    layout = row(controlers, p_column)
    panel = Panel(child=layout, title='Return Analysis')

    return panel