import Moises.chroma.dbconfig as dbconfig
from Moises.create_log import log

import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_db():
    client = chromadb.PersistentClient(path=dbconfig.db_name)
    collection = client.create_collection(name=dbconfig.collection_name)
    log("DB created")


def get_db() -> tuple:
    # Initialize Chroma DB client
    client = chromadb.PersistentClient(path=f'{dbconfig.db_name}')
    collection = client.get_collection(name=dbconfig.collection_name)
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    log('DB accessed')

    return client, collection, embeddings

