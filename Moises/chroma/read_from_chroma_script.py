from Moises.chroma.chromadb_init import get_db


def get_data():
    # Initialize Chroma DB client
    client, collection, embeddings = get_db()

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
