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

'''try:
    conn = connect_database()
    if conn is None:
        print("A conexão não foi estabelecida.")
    else:
        print("Conexão estabelecida com sucesso.")
except duckdb.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

df_estados = conn.execute('SELECT * FROM covid19_estados').df()
df_municipios = conn.execute('SELECT * FROM covid19_municipios').df()
df_brasil = conn.execute('SELECT * FROM covid19_brasil').df()'''

estados_brasil = load_file_json('geojson/brazil_geo.json')
df_estados, df_municipios, df_brasil = transform()

# ======================================================
# Instanciação do dash
app =  dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG]) # Setando o tema da aplicação

fig = px.choropleth_mapbox(df_estados, locations='estado', color='casosnovos',
                            center={'lat': -16.95, 'lon': -47.78},
                            geojson=estados_brasil, color_continuous_scale='Redor', opacity=0.4,
                            hover_data={
                                'casosacumulado': True,
                                'casosnovos': True,
                                'obitosnovos': True,
                                'estado': True
                            }) # elemento que vai conter nosso mapa
fig.update_layout(
    mapbox_style='carto-darkmatter'
)

# ======================================================
# Construção do layout
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='choropleth-map', figure=fig)
        ])
    ])
)

if __name__ == '__main__':
    app.run_server(debug=True)