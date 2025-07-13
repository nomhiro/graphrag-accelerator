import os
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
import azure.cosmos.partition_key as partition_key

# CosmosDBの接続情報
COSMOS_DB_URL = "https://cosmos-rag-extra-1.documents.azure.com:443/"
COSMOS_DB_KEY = "W3FMpdaTFYkjhRicxcbLG2ofk3YzX7sBYFvdMgB8uBTPdJ539DRvkF92SuL66xSWipQxLr8Ja8DYACDbFa4GiQ=="
DATABASE_NAME = "doc-db"
CONTAINER_NAME = "doc-container"

# CosmosDBクライアントの初期化
client = cosmos_client.CosmosClient(COSMOS_DB_URL, {'masterKey': COSMOS_DB_KEY})
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

# SQLクエリの実行
# query = "SELECT c.content FROM c WHERE CONTAINS(c.file_name, \"お手入れ読本\") ORDER BY c.page_number"
query = "SELECT c.content FROM c"
items = list(container.query_items(query=query, enable_cross_partition_query=True))

# 出力ディレクトリの作成
output_dir = "./data/"
os.makedirs(output_dir, exist_ok=True)

# 結果をmdファイルに出力
for idx, item in enumerate(items):
    filename = os.path.join(output_dir, f"お手入れ_{idx + 1}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"# Item {idx + 1}\n")
        for key, value in item.items():
            file.write(f"## {key}\n")
            file.write(f"{value}\n\n")

print("ファイルの出力が完了しました。")