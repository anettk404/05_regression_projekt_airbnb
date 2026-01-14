import pandas as pd
import plotly.graph_objects as go

def create_airbnb_usa_map():
    # DATEN Karte USA (Jetzt innerhalb der Funktion)
    data = {
        "City": ["Albany", "Asheville", "Austin", "Boston", "Bozeman", "Chicago", "Columbus", "Dallas", 
                 "Denver", "Fort Worth", "Los Angeles", "Nashville", "New Orleans", "New York City", 
                 "Portland", "San Diego", "San Francisco", "Seattle", "Washington, D.C."],
        "State": ["NY", "NC", "TX", "MA", "MT", "IL", "OH", "TX", "CO", "TX", "CA", "TN", "LA", "NY", 
                  "OR", "CA", "CA", "WA", "DC"],
        "Lat": [42.6526, 35.5951, 30.2672, 42.3601, 45.6770, 41.8781, 39.9612, 32.7767, 39.7392, 32.7555, 
                34.0522, 36.1627, 29.9511, 40.7128, 45.5152, 32.7157, 37.7749, 47.6062, 38.9072],
        "Lon": [-73.7562, -82.5515, -97.7431, -71.0589, -111.0429, -87.6298, -90.0715, -96.7970, 
                -104.9903, -97.3308, -118.2437, -86.7816, -90.0715, -74.0060, -122.6784, -117.1611, 
                -122.4194, -122.3321, -77.0369]
    }

    df = pd.DataFrame(data)

    # Text-Offsets individuell setzen
    df['TextPosition'] = 'middle right'
    df['TextDx'] = 2
    df['TextDy'] = 0 

    df.loc[df['City'] == 'Boston', ['TextPosition','TextDx','TextDy']] = ['middle left', -10, 5]
    df.loc[df['City'] == 'Dallas', 'TextDx'] = 10
    df.loc[df['City'] == 'Fort Worth', ['TextPosition','TextDx','TextDy']] = ['middle left', -10, -5]
    df.loc[df['City'] == 'Albany', ['TextPosition','TextDx','TextDy']] = ['top right', 5, 5]

    # Markerfarbe und -größe
    df['MarkerColor'] = '#FF6F61'
    df['MarkerSize'] = 10 

    df.loc[df['City'] == 'New York City', 'MarkerColor'] = 'teal'
    df.loc[df['City'] == 'New York City', 'MarkerSize'] = 16

    # Plotly Karte
    fig = go.Figure(data=[
        go.Scattergeo(
            locationmode='USA-states',
            lat=df['Lat'],
            lon=df['Lon'],
            mode='markers+text',
            marker=dict(
                size=df['MarkerSize'],
                opacity=0.8,
                line=dict(width=1, color='White'),
                color=df['MarkerColor']
            ),
            text=df['City'],
            textfont=dict(size=10, color='Black'),
            textposition=df['TextPosition'],
            texttemplate="%{text}",
            hoverinfo='text',
            hovertext=df['City'] + '<br>' + df['State']
        )
    ])

    fig.update_layout(
        title='Datenquelle: Inside Airbnb USA',
        height=650,
        width=900,
        geo=dict(
            scope='usa',
            landcolor="rgb(240, 240, 240)",
            subunitcolor="White",
            showland=True,
        ),
        template="plotly_white",
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    # GANZ WICHTIG: Das Objekt zurückgeben, statt fig.show()
    return fig

