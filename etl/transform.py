import os
import sys
import duckdb
from typing import Tuple, List, Optional, Any

sys.path.insert(0, os.getcwd())
from database import connect_database

def connect_to_database() -> Optional[duckdb.DuckDBPyConnection]:
    try:
        conn = connect_database()
        print("Connection was not established." if conn is None else "Connection established successfully.")
        return conn
    except duckdb.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def extract_covid19_data(conn: duckdb.DuckDBPyConnection, query: str) -> Tuple[duckdb.DuckDBPyRelation, duckdb.DuckDBPyRelation, duckdb.DuckDBPyRelation]:
    """
    
    Args:
        conn: Conexão com o banco de dados.
        query: Consulta base para extração de dados.

    Returns:
        Uma tupla com DataFrames de dados de estados, municípios e Brasil.
    """
    df_states = conn.execute(f'''
        SELECT regiao, estado, coduf, _data, semanaepi, populacaotcu2019, casosacumulado, casosnovos, obitosacumulado, obitosnovos, recuperadosnovos, emacompanhamentonovos
        FROM ({query})
        WHERE estado IS NOT NULL AND codmun IS NULL
        LIMIT 5000
    ''').df()

    df_cities = conn.execute(f'''
        SELECT *
        FROM ({query})
        WHERE municipio IS NOT NULL AND codmun IS NOT NULL
        LIMIT 5000
    ''').df()

    df_brazil = conn.execute(f'''
        SELECT regiao, coduf, _data, semanaepi, populacaotcu2019, casosacumulado, casosnovos, obitosacumulado, obitosnovos, recuperadosnovos, emacompanhamentonovos
        FROM ({query})
        WHERE regiao = 'Brasil'
        LIMIT 5000
    ''').df()

    return df_states, df_cities, df_brazil

def register_dataframe(conn: duckdb.DuckDBPyConnection, df: duckdb.DuckDBPyRelation, df_name: str) -> None:
    """
    
    Args:
        conn: Conexão com o banco de dados.
        df: DataFrame a ser registrado.
        df_name: Nome do DataFrame.
    """
    try:
        conn.register(df_name, df)
        print(f"DataFrame '{df_name}' registered successfully.")
    except Exception as e:
        print(f"Error registering DataFrame '{df_name}': {e}")

def create_table(conn: duckdb.DuckDBPyConnection, table_name: str) -> None:
    """
    
    Args:
        conn: Conexão com o banco de dados.
        table_name: Nome da tabela a ser criada.
    """
    try:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM {table_name}")
        print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table '{table_name}': {e}")

def export_table_to_csv(conn: duckdb.DuckDBPyConnection, table_name: str, file_name: str, silver_csv_folder_path: str) -> None:
    """
    
    Args:
        conn: Conexão com o banco de dados.
        table_name: Nome da tabela a ser exportada.
        file_name: Nome do arquivo CSV.
        silver_csv_folder_path: Caminho para a pasta onde o arquivo CSV será salvo.
    """
    if not os.path.exists(silver_csv_folder_path):
        os.makedirs(silver_csv_folder_path)

    csv_file_path = os.path.join(silver_csv_folder_path, f"{file_name}.csv")

    try:
        conn.execute(f"COPY {table_name} TO '{csv_file_path}' (HEADER, DELIMITER ';')")
        print(f"Table '{table_name}' exported to CSV.")
    except Exception as e:
        print(f"Error exporting table '{table_name}' to CSV: {e}")

def transform() -> Tuple[duckdb.DuckDBPyRelation, duckdb.DuckDBPyRelation, duckdb.DuckDBPyRelation]:
    """
    
    Returns:
        Uma tupla com os DataFrames de estados, municípios e Brasil.
    """
    root_folder = os.getcwd()
    folder_bronze = os.path.join(root_folder, 'data', 'extracted_files')
    path_bronze_files = os.path.join(folder_bronze, '*')
    folder_gold = os.path.join(root_folder, 'data', 'silver_csv_files')
    
    query_base = f'''
        SELECT *
        FROM read_csv_auto(
            '{path_bronze_files}',
            normalize_names=True,
            ignore_errors=True,
            delim=';',
            header=True
        )
    '''
    
    df_names = ['covid19_states', 'covid19_cities', 'covid19_brazil']

    conn = connect_to_database()
    dataframes = extract_covid19_data(conn, query_base)
    
    for df, df_name in zip(dataframes, df_names):
        register_dataframe(conn, df, df_name)
        create_table(conn, df_name)
        export_table_to_csv(conn, df_name, df_name, folder_gold)
    
    return dataframes

transform()