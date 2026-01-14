import pandas as pd
import numpy as np
import logging
import warnings
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, HoverTool
from bokeh.palettes import Viridis256
from bokeh.io import output_notebook
from bokeh.util.warnings import BokehDeprecationWarning, BokehUserWarning

def create_nyc_price_map(df):
    """
    Erstellt eine interaktive Bokeh-Karte für NYC Preise.
    Erwartet einen Dataframe mit 'longitude', 'latitude' und 'price'.
    """
    # 1. Warnings & Logging stumm schalten
    warnings.filterwarnings("ignore", category=BokehDeprecationWarning)
    warnings.filterwarnings("ignore", category=BokehUserWarning)
    logging.getLogger('bokeh').setLevel(logging.ERROR)

    # WICHTIG: Im Modul brauchen wir output_notebook() meist nicht, 
    # das rufen wir besser einmalig im Notebook auf.

    # 2. Interne Hilfsfunktion zur Umrechnung
    def lnglat_to_meters(longitude, latitude):
        origin_shift = 2 * np.pi * 6378137 / 2.0
        mx = longitude * origin_shift / 180.0
        my = np.log(np.tan((90 + latitude) * np.pi / 360.0)) / (np.pi / 180.0)
        my = my * origin_shift / 180.0
        return mx, my

    # 3. Daten vorbereiten
    df_map = df.copy()
    df_map['x'], df_map['y'] = lnglat_to_meters(df_map['longitude'], df_map['latitude'])

    # 4. Color Mapper definieren (Preisdeckel bei 564$ wie in deiner Analyse)
    color_mapper = LinearColorMapper(palette=Viridis256, low=df_map.price.min(), high=564)

    # 5. Figure erstellen
    p = figure(title="Airbnb NYC - Preisdichte & geografische Verteilung", 
               x_axis_type="mercator", y_axis_type="mercator",
               height=700, width=900,
               tools="pan,wheel_zoom,box_zoom,reset")

    p.add_tile("CARTODBPOSITRON") 

    source = ColumnDataSource(df_map)

    # 6. Datenpunkte hinzufügen
    p.circle(x='x', y='y', size=4, 
             fill_alpha=0.6, 
             source=source,
             fill_color={'field': 'price', 'transform': color_mapper},
             line_color=None)

    # 7. Farblegende & Hover
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, location=(0,0), title="Preis $")
    p.add_layout(color_bar, 'right')

    hover = HoverTool(tooltips=[
        ("Preis", "@price$"),
        ("Stadtteil", "@neighbourhood_group_cleansed"),
        ("Zimmertyp", "@room_type")
    ])
    p.add_tools(hover)

    return p