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
import json
import sys
import os

sys.path.insert(0, os.getcwd())
from database import connect_database

def separate_covid19_data(conn, q):
    df_estados = conn.execute(f'''
        SELECT regiao, estado, coduf, _data, semanaepi, populacaotcu2019, casosacumulado, casosnovos, obitosacumulado, obitosnovos, recuperadosnovos,  emacompanhamentonovos
        FROM ({q})
        WHERE 
            estado IS NOT NULL AND
            codmun IS NULL
    ''').df()

    df_municipios = conn.execute(f'''
        SELECT *
        FROM ({q})
        WHERE codmun IS NOT NULL
    ''').df()

    df_brasil = conn.execute(f'''
        SELECT regiao, coduf, _data, semanaepi, populacaotcu2019, casosacumulado, casosnovos, obitosacumulado, obitosnovos, recuperadosnovos,  emacompanhamentonovos
        FROM ({q})
        WHERE regiao = 'Brasil'
    ''').df()

    return df_estados, df_municipios, df_brasil

def register_dataframes(conn, df_estados, df_municipios, df_brasil):
    try:
        conn.register('covid19_estados', df_estados)
        conn.register('covid19_municipios', df_municipios)
        conn.register('covid19_brasil', df_brasil)
        print(f'Registrou todos DataFrame na conexão com sucesso!')
    except Exception as e:
        print(f'Erro ao registrar tabela: {e}')

def create_table_db(list_name_tables):
    try:
        print('entrou aqui')
        for name_table in list_name_tables:
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {name_table} AS SELECT * FROM {name_table}
            ''')
        print(f'Tabela criada com sucesso!')
    except BaseExceptionGroup as e:
        print(f'Erro ao criar tabela: {e}')

def describe_covid19_tables():
    result_estados = conn.execute(f'DESCRIBE covid19_estados').df()
    result_municipios = conn.execute(f'DESCRIBE covid19_municipios').df()
    result_brasil = conn.execute(f'DESCRIBE covid19_brasil').df()


if __name__ == '__main__':
    root_folder = os.getcwd()
    bronze_data_folder = os.path.join(root_folder, 'data', 'extracted_files')
    full_bronze_data_path = os.path.join(bronze_data_folder, '*')

    list_name_tables = ['covid19_estados', 'covid19_municipios', 'covid19_brasil']
    
    try:
        conn = connect_database()
        if conn is None:
            print("A conexão não foi estabelecida.")
        else:
            print("Conexão estabelecida com sucesso.")
    except duckdb.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    q = f'''SELECT * FROM read_csv_auto(
                '{full_bronze_data_path}',
                normalize_names=true,
                ignore_errors=true,
                delim=';',
                header=true
            )'''
    
    df_estados, df_municipios, df_brasil = separate_covid19_data(conn, q)
    register_dataframes(conn, df_estados, df_municipios, df_brasil)
    create_table_db(list_name_tables)