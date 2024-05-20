import dbconfig
import chromadb
from Moises.main import log

def create_db():
    client = chromadb.PersistentClient(path=dbconfig.db_name)
    collection = client.create_collection(name=dbconfig.collection_name)
    log("DB created")

