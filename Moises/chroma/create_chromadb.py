import config
import chromadb

client = chromadb.PersistentClient(path=config.db_name)
collection = client.create_collection(name=config.collection_name)
print("db created")

