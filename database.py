import duckdb

def connect_database():
    return duckdb.connect(database='dbcovid19.db', read_only=False)