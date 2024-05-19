import config
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize Chroma DB client
client = chromadb.PersistentClient(path=config.db_name)
collection = client.get_collection(name=config.collection_name)


embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

# Get user input
query = input("Enter your query: ")

# Convert query to vector representation
query_vector = embeddings.embed_query(query)

# Query Chroma DB with the vector representation
results = collection.query(query_embeddings=query_vector, n_results=5)

# Print results
print(results['ids'])

for result in results["documents"]:
   for i in result:
       print(i)