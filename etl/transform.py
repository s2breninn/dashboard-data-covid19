import duckdb
import sys
import os

print(os.getcwd())
sys.path.insert(0, os.getcwd())
from database import connect_database

def separate_covid19_data(conn, q):
    df_estados = conn.execute(f'''
        SELECT regiao, estado, coduf, _data, semanaepi, populacaotcu2019, casosacumulado, casosnovos, obitosacumulado, obitosnovos, recuperadosnovos,  emacompanhamentonovos
        FROM ({q})
        WHERE 
            estado IS NOT NULL AND
            codmun IS NULL
        LIMIT 5000
    ''').df()

    df_municipios = conn.execute(f'''
        SELECT *
        FROM ({q})
        WHERE 
            municipio IS NOT NULL AND
            codmun IS NOT NULL
        LIMIT 5000
    ''').df()

    df_brasil = conn.execute(f'''
        SELECT regiao, coduf, _data, semanaepi, populacaotcu2019, casosacumulado, casosnovos, obitosacumulado, obitosnovos, recuperadosnovos,  emacompanhamentonovos
        FROM ({q})
        WHERE regiao = 'Brasil'
        LIMIT 5000
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

def create_table_db(conn, list_name_tables: list, data_gold_csv):
    try:
        for name_table in list_name_tables:
            conn.execute(f'CREATE TABLE IF NOT EXISTS {name_table} AS FROM {name_table}')
            to_csv(conn, name_table, name_table, data_gold_csv)
            q = conn.execute(f'SELECT * FROM {name_table}').df()
            print(q)
            print(f'Tabela {name_table} criada com sucesso!')
    except BaseExceptionGroup as e:
        print(f'Erro ao criar tabela: {e}')

def describe_covid19_tables(conn):
    result_estados = conn.execute(f'DESCRIBE covid19_estados').df()
    result_municipios = conn.execute(f'DESCRIBE covid19_municipios').df()
    result_brasil = conn.execute(f'DESCRIBE covid19_brasil').df()

def to_csv(conn, name_table, name_file, path_data_gold_csv):
    if not os.path.exists(path_data_gold_csv):
        os.makedirs(path_data_gold_csv)

    path_data_gold_csv = os.path.join(path_data_gold_csv, name_file)
    conn.execute(f"COPY {name_table} TO '{path_data_gold_csv}.csv' (HEADER, DELIMITER ';')")

def transform():
    root_folder = os.getcwd()
    bronze_data_folder = os.path.join(root_folder, 'data', 'extracted_files')
    full_bronze_data_path = os.path.join(bronze_data_folder, '*')
    data_gold_csv = os.path.join(root_folder, 'data', 'gold_csv_files')
    
    list_name_tables = ['covid19_estados', 'covid19_municipios', 'covid19_brasil']

    try:
        conn = connect_database()
        if conn is None:
            print("A conexão não foi estabelecida.")
        else:
            print("Conexão estabelecida com sucesso.")
    except duckdb.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    q = f'''SELECT * 
            FROM read_csv_auto(
                '{full_bronze_data_path}',
                normalize_names=true,
                ignore_errors=true,
                delim=';',
                header=true
            )'''
    
    df_estados, df_municipios, df_brasil = separate_covid19_data(conn, q)
    register_dataframes(conn, df_estados, df_municipios, df_brasil)
    create_table_db(conn, list_name_tables, data_gold_csv)
    print('Passou pelas funções todas. funcionou')

    return df_estados, df_municipios, df_brasil # DataFrames criados dos estados, municipios e do Brasil