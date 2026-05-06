import pandas as pd
from sqlalchemy import create_engine
import clickhouse_connect
import logging


from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")
# -------------------------------
# CONFIG
# -------------------------------

MYSQL_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

CH_CONFIG = {
    "host": os.getenv("CH_HOST"),
    "port": 8443,
    "username": os.getenv("CH_USER"),
    "password": os.getenv("CH_PASSWORD"),
    "database": os.getenv("CH_DATABASE"),
    "secure": True
}

CH_DATABASE = "default"

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(level=logging.INFO)

# -------------------------------
# CONNECTORS
# -------------------------------
def get_mysql_engine():
    return create_engine(MYSQL_URI)

def get_clickhouse_client():
    return clickhouse_connect.get_client(**CH_CONFIG)

# -------------------------------
# GET ALL TABLES
# -------------------------------
def get_tables(engine):
    query = "SHOW TABLES"
    tables = pd.read_sql(query, engine)
    return tables.iloc[:, 0].tolist()

# -------------------------------
# EXTRACT (CHUNKED)
# -------------------------------
def extract(engine, table_name, chunksize=10000):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine, chunksize=chunksize)

# -------------------------------
# TRANSFORM
# -------------------------------
def transform(df):
    df = df.drop_duplicates()
    df = df.fillna(method="ffill")

    df = df.convert_dtypes()

    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

   

    return df

# -------------------------------
# DTYPE MAPPING (IMPORTANT)
# -------------------------------
import pandas as pd

def map_dtype(dtype):

    if pd.api.types.is_integer_dtype(dtype):
        return "Int64"
    elif pd.api.types.is_float_dtype(dtype):
        return "Float64"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DateTime"
    else:
        return "String"

# -------------------------------
# CREATE TABLE DYNAMICALLY
# -------------------------------
def create_table(client, df, table_name):
    columns = []
     # 🔥 ADD THIS LINE HERE
    client.command(f"DROP TABLE IF EXISTS {CH_DATABASE}.{table_name}")

    for col, dtype in df.dtypes.items():
        ch_type = map_dtype(dtype)
        columns.append(f"`{col}` {ch_type}")

    schema = ", ".join(columns)

    create_query = f"""
    CREATE TABLE IF NOT EXISTS {CH_DATABASE}.{table_name} (
        {schema}
    )
    ENGINE = MergeTree()
    ORDER BY tuple()
    """

    client.command(create_query)

# -------------------------------
# LOAD
# -------------------------------

def load(client, df, table_name):
    # 🔥 Convert to list of rows (correct format)
    data = df.values.tolist()

    client.insert(
        table=f"{CH_DATABASE}.{table_name}",
        data=data,
        column_names=list(df.columns)
    )
# -------------------------------
# MAIN PIPELINE
# -------------------------------
def run_etl():
    engine = get_mysql_engine()
    client = get_clickhouse_client()

    tables = get_tables(engine)
    logging.info(f"Found tables: {tables}")

    for table in tables:
        logging.info(f"Processing table: {table}")

        for chunk in extract(engine, table):
            chunk = transform(chunk)

            create_table(client, chunk, table)
            load(client, chunk, table)

        logging.info(f"Finished table: {table}")

    logging.info("ETL Pipeline Completed Successfully")


if __name__ == "__main__":
    run_etl()