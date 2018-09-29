from bokeh.models.widgets import (
    Select, Slider, RadioButtonGroup, RangeSlider)

map_widget_types = {
    'Select': Select,
    'RadioButtonGroup': RadioButtonGroup,
    'Slider': Slider,
    'RangeSlider': RangeSlider
}

def create_widget(setting):
    widget = map_widget_types[setting['type']]
    widget = widget(**setting['specs'])
    return widget