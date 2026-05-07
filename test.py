import clickhouse_connect
import os
from dotenv import load_dotenv
load_dotenv()
import logging



client = clickhouse_connect.get_client(
    host="f7byvl6pzu.asia-southeast1.gcp.clickhouse.cloud",
    port=8443,
    username="default",
    password="pWZEEvA06JyH~",
    secure=True
)

print(client.query("SELECT 1"))
result = client.query("SELECT 1")
print(result.result_rows)
print(os.getenv("CH_PASSWORD"))



