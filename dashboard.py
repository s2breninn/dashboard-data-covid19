import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import duckdb
import sys
import os

sys.path.insert(0, os.getcwd())
from database import connect_database
from utils.load_file_json import load_file_json
from etl.transform import transform

estados_brasil = load_file_json('geojson/brazil_geo.json')
#df_estados, df_municipios, df_brasil = transform()

df_states = pd.read_csv('data/gold_csv_files/covid19_estados.csv', sep=';')
df_brazil = pd.read_csv('data/gold_csv_files/covid19_brasil.csv', sep=';')
df_data = df_states[df_states['estado'] == 'RJ']

# ======================================================
# Instanciação do dash
app =  dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG]) # Setando o tema da aplicação

fig = px.choropleth_mapbox(df_states, locations='estado', color='casosnovos',
                            center={'lat': -16.95, 'lon': -47.78}, zoom=4,
                            geojson=estados_brasil, color_continuous_scale='Redor', opacity=0.4,
                            hover_data={
                                'casosacumulado': True,
                                'casosnovos': True,
                                'obitosnovos': True,
                                'estado': True
                            }) # elemento que vai conter nosso mapa
fig.update_layout(
    paper_bgcolor='#242424',
    autosize=True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style='carto-darkmatter'
)

fig2 = go.Figure(layout={'template': 'plotly_dark'})
fig2.add_trace(go.Scatter(x=df_data['_data'], y=df_data['casosacumulado']))
fig2.update_layout(
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    autosize=True,
    margin=dict(l=0, r=10, t=10, b=10)
)

# ======================================================
# Construção do layout
app.layout = dbc.Container(
    dbc.Row([

        dbc.Col([
            html.Div([
                html.Img(id='logo', src=app.get_asset_url('logo_dark.png'), height=50),
                html.H5('Evolução COVID-19'),
                dbc.Button('BRASIL', color='primary', id='location-button', size='lg')    
            ], style={}),
            html.P('Informe a data na qual deseja obter informações:', style={'margin-top': '40px'}),
            html.Div(id='div-test', children=[
                dcc.DatePickerSingle(
                    id='date-picker',
                    min_date_allowed=df_brazil['_data'].min(),
                    max_date_allowed=df_brazil['_data'].max(),
                    initial_visible_month=df_brazil['_data'].min(),
                    date=df_brazil['_data'].max(),
                    display_format='MMMM D, YYYY',
                    style={'border': '0px solid black'}
                )
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos recuperados'),
                            html.H3(style={'color': '#adfc92'}, id='casos-recuperados-text'),
                            html.Span('Em acompanhamento'),
                            html.H5(id='em-acompanhamento-text')
                        ], color='light', outline=True, style={'margin-top': '10px', 'box-shadow': '0 4px 4px 0  rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.14)', 'color': '#ffffff'})
                    ], md=12)
                ])
            ]),
            
            dcc.Graph(id='line-graph', figure=fig2)
        ]),
        dbc.Col([
            dcc.Graph(id='choropleth-map', figure=fig)
        ])
    ])
)

if __name__ == '__main__':
    app.run_server(debug=True)