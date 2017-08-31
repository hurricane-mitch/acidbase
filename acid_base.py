# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 08:21:32 2016

@author: Mitchell Huot
"""

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, TextInput
from bokeh.plotting import Figure, curdoc
from bokeh.models.widgets import Button
from titration_class import Titration
import numpy as np

def update(text1, text2, text3, text4, text5, text6):
    acid_pKa = np.power(10, -float(text1.value))
    acid_conc = float(text2.value)
    acid_vol = float(text3.value)
    titrant_conc = float(text4.value)
    Kw = float(text5.value)
    base_vol = float(text6.value)
    global curve
    curve = Titration(acid_pKa, acid_conc, acid_vol, titrant_conc, Kw, base_vol)
    source.data = dict(
        x= curve.x,
        y=curve.y,
        
    )

def callback():
    update_vol(text7, curve)

def update_vol(text1, curve):
    if text1 != 0:
        curve.add_base(float(text1.value))
        source.data = dict(
        x= curve.x,
        y=curve.y,      
    )


text1 = TextInput(title="Acid pKa", value="2.8")
text2 = TextInput(title="Acid concentration (M)", value="1.00E-02")
text3 = TextInput(title="Acid Volume (mL)", value="30.0")
text4 = TextInput(title="Titrant Concentration (M)", value="1.00E-02")
text5 = TextInput(title="Kw", value="1.01E-14")
text6 = TextInput(title="Base Volume titrated (mL)", value="0.0")

text7 = TextInput(title="Amount of base titrated (mL)", value="1.00")
button1 = Button(label="Titrate")

source = ColumnDataSource(data=dict(x=[], y=[]))


plot = Figure(plot_width=400, plot_height=400, title="Titration of a weak acid")
plot.circle(x="x", y="y", source=source, line_width=3, line_alpha=0.6)
plot.xaxis.axis_label="mL titrant"
plot.yaxis.axis_label="pH"

controls = [text1, text2, text3, text4, text5, text6]
for control in controls:
    control.on_change('value', lambda attr, old, new: update(text1, text2, text3, text4, text5, text6))

button1.on_click(callback)

update(text1, text2, text3, text4, text5, text6)



layout = column(text1, text2, text3, text4, text5, text6, plot, text7, button1)
curdoc().add_root(layout)

