from pymongo import MongoClient

class Repository:
    def __init__(self, db_url, db_name, collection_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_one(self, data):
        return self.collection.insert_one(data)

    def find_one(self, query):
        return self.collection.find_one(query)

    def find_many(self, query):
        return list(self.collection.find(query))

    def update_one(self, query, new_values):
        return self.collection.update_one(query, {'$set': new_values})

    def delete_one(self, query):
        return self.collection.delete_one(query)

    def delete_many(self, query):
        return self.collection.delete_many(query)

    def count_documents(self, query):
        return self.collection.count_documents(query)
    
    def bulk_insert(self, data_list):
        """
        Insere uma lista de objetos (data_list) no banco de dados em formato de "bulk insert".
        """
        if not isinstance(data_list, list):
            raise ValueError("O parâmetro data_list deve ser uma lista de objetos.")

        if len(data_list) == 0:
            raise ValueError("A lista data_list não pode estar vazia.")

        try:
            result = self.collection.insert_many(data_list)
            return result.inserted_ids
        except Exception as e:
            raise RuntimeError(f"Erro ao realizar o bulk insert: {str(e)}")