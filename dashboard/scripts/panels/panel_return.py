import json
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column, row, WidgetBox
from bokeh.models import ColumnDataSource, Panel, HoverTool
from bokeh.palettes import Category10_10
from dashboard.scripts.widgets import create_widget
from dashboard.scripts.plot import plot_histogram
from dashboard.scripts.utility import Slice

with open('dashboard/scripts/json/widgets.json') as json_widgets:
    widget_settings = json.load(json_widgets)
    widget_settings = widget_settings['panel_return']

settings_figure = {
    'plot_width': 500, 
    'plot_height': 500, 
    'title': 'Test Hitogram',
    'x_axis_label': 'Return', 
    'y_axis_label': 'Proportion'
}

def panel_return(data):

    def get_data():
        name_column_period = selector_test.value
        name_column_quantile = \
            selector_quantile.labels[selector_quantile.active]
        unique_quantiles = data[name_column_quantile].unique()
        bins = int(selector_bins.value)
        

        by_quantile = pd.DataFrame(
            columns=['proportion', 'left', 'right', 'name', 'color']
        )

        for i, quantile in enumerate(sorted(unique_quantiles)):
            subset = data[data[name_column_quantile] == quantile]
            hist, edges = np.histogram(subset[name_column_period], bins=bins)
            sub_df = pd.DataFrame(
                {
                    'proportion': hist / np.sum(hist),
                    'left': edges[:-1], 
                    'right': edges[1:],
                    'name': name_column_quantile,
                    'color': Category10_10[i]
                }
            )
            by_quantile = by_quantile.append(sub_df)

        by_quantile = by_quantile.sort_values(['name', 'left'])

        return ColumnDataSource(by_quantile)

    def draw(source):
        ### Create a figure ###
        p = figure(
            plot_width=settings_figure['plot_width'], 
            plot_height=settings_figure['plot_height'], 
            title=settings_figure['title'],
            x_axis_label=settings_figure['x_axis_label'], 
            y_axis_label=settings_figure['y_axis_label']
        )

        p.quad(
            source=source, bottom=0, top='proportion', 
            left='left', right='right',
			color='color', legend='name',
            hover_fill_color='color',
            fill_alpha = 0.7, hover_fill_alpha=1.0, line_color='black'
        )

        hover = HoverTool(tooltips=[('Quantile', '@name')],mode='vline')
        p.add_tools(hover)

        return p

    def update():
        source_updated = get_data()
        source.data = source_updated.data

    selector_test = create_widget(widget_settings['test'])
    selector_period = create_widget(widget_settings['period'])
    selectort_metric = create_widget(widget_settings['metric'])
    selector_quantile = create_widget(widget_settings['quantile'])
    selector_bins = create_widget(widget_settings['bins'])

    selector_period.on_change('value', lambda attr, old, new: update())
    selector_quantile.on_change('active', lambda attr, old, new: update())
    selector_bins.on_change('value', lambda attr, old, new: update())
    
    source = get_data()
    p = draw(source)

    ### Setting up the laytou ###
    # Widgets
    controlers = WidgetBox(
        selector_test,
        selector_period,
        selectort_metric,
        selector_quantile,
        selector_bins,
        width=350
    )

    # Layout
    layout = row(controlers, p)
    panel = Panel(child=layout, title='Return Analysis')

    return panel