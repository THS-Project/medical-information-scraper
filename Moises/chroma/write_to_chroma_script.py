import textwrap
import chromadb
import os
import uuid
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", " ", ""],
    chunk_size=1000,
    chunk_overlap=100)

#embeddings = SentenceTransformerEmbeddingFunction()
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

# Initialize chroma db client
client = chromadb.PersistentClient(path="./db1")
collection = client.create_collection(name="collection1")
print("db created")

# process each JSON in the /json_management/scraped_json directory
directory = '../json_management/scraped_json'
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r') as json_file:
            data = json.load(json_file)
            context_value = data.get('context')[0]

            # split text into chunks
            chunks = text_splitter.split_text(context_value)

            # Convert chunks to vector representations and store in chroma db
            documents_list = []
            embeddings_list = []
            ids = []

            for i, chunk in enumerate(chunks):
                vector = embeddings.embed_query(chunk)

                documents_list.append(chunk)
                embeddings_list.append(vector)
                curid = str(uuid.uuid4())
                ids.append(curid)


            collection.add(
                embeddings=embeddings_list,
                documents=documents_list,
                ids=ids
            )

            data['chunk_id'] = ids
            data['chunks'] = chunks

            with open(os.path.join(directory, filename), 'w') as json_file:
                json.dump(data, json_file)