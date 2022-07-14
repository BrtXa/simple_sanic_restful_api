import pymongo


class MongoDB:
    def __init__(self, URI, DB_NAME) -> None:
        client = pymongo.MongoClient(URI)
        self.db = client[DB_NAME]

    # Basic methods for CRUD operations.
    ########################################
    # Create new document (Insert documents).
    def create_data(self, collection_name: str, new_doc: list[dict]):
        collection = self.db[collection_name]
        collection.insert_one(new_doc)

    # Get documents from the database (Read/query documents).
    def read_data(self, collection_name: str, filter: dict):
        collection = self.db[collection_name]
        documents = collection.find_one(filter)
        return documents

    # Update documents from the database (Update documents).
    def update_data(self, collection_name: str, filter: dict, update: dict):
        collection = self.db[collection_name]
        collection.update_many(filter, {"$set": update}, upsert=True)

    # Delete documents based on specified filter.
    def delete_data(self, collection_name: str, filter: dict):
        collection = self.db[collection_name]
        collection.delete_many(filter)
