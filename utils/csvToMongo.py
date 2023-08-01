import pandas as pd
from pymongo import MongoClient

def save_csv_to_mongodb(file_path, collection_name,database_name, mongodb_uri):
    # Ler o arquivo CSV usando pandas
    df = pd.read_csv(file_path)

    # Conectar-se ao MongoDB
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Converter o DataFrame para formato JSON
    data_json = df.to_dict(orient='records')
    print(data_json)
    # Inserir os registros no MongoDB
    collection.insert_many(data_json)

    # Fechar a conexão com o MongoDB
    client.close()

# Exemplo de uso
if __name__ == "__main__":
    file_path = 'data.csv'
    collection_name = 'eletricalAsset'
    mongodb_uri = 'mongodb://localhost:27017/'

    save_csv_to_mongodb(file_path, collection_name,'sequencia', mongodb_uri)
