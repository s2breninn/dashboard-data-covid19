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

select_columns = {
    'casosacumulados': 'Casos Acumulados',
    'casosnovos': 'Casos Novos',
    'obitosacumulados': 'Obitos Totais',
    'obitosnovos': 'Obitos por dia'
}

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
                dbc.Col([dbc.Card([   
                        dbc.CardBody([
                            html.Span("Casos recuperados", className="card-text"),
                            html.H3(style={"color": "#adfc92"}, id="casos-recuperados-text"),
                            html.Span("Em acompanhamento", className="card-text"),
                            html.H5(id="em-acompanhamento-text"),
                            ])
                        ], color="light", outline=True, style={"margin-top": "10px",
                                "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                "color": "#FFFFFF"})], md=4),
                dbc.Col([dbc.Card([   
                        dbc.CardBody([
                            html.Span("Casos confirmados totais", className="card-text"),
                            html.H3(style={"color": "#389fd6"}, id="casos-confirmados-text"),
                            html.Span("Novos casos na data", className="card-text"),
                            html.H5(id="novos-casos-text"),
                            ])
                        ], color="light", outline=True, style={"margin-top": "10px",
                                "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                "color": "#FFFFFF"})], md=4),
                dbc.Col([dbc.Card([   
                        dbc.CardBody([
                            html.Span("Óbitos confirmados", className="card-text"),
                            html.H3(style={"color": "#DF2935"}, id="obitos-text"),
                            html.Span("Óbitos na data", className="card-text"),
                            html.H5(id="obitos-na-data-text"),
                            ])
                        ], color="light", outline=True, style={"margin-top": "10px",
                                "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                "color": "#FFFFFF"})], md=4),
            ]),
            dbc.Row([

            ]),

            html.Div([
                html.P('Selecione que tipo de dado deseja visualizar:', style={'margin-top': '25px'}),
                dcc.Dropdown(id='location-dropdown',
                             options=[{'label': j, 'value': i} for i, j in select_columns.items()],
                             value='casosnovos',
                             style={'margin-top': '10px'}
                             ),
                dcc.Graph(id='line-graph', figure=fig2)
            ])

        ], md=4, style={"padding": "25px", "background-color": '#242424'}),
        
        dbc.Col([
            dcc.Loading(id='loading-1', type='default', 
                        children=[
                            dcc.Graph(id='choropleth-map', figure=fig, style={"height": "100vh", "marin-right": "10px"})
                        ])
        ], md=7),
    ])
, fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)