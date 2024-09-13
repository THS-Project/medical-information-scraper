from Moises.chroma.chromadb_init import get_db


def get_data(query=None) -> list:
    # Initialize Chroma DB client
    client, collection, embeddings = get_db()

    # Get user input
    if query is None:
        query = input("Enter your query: ")

    # Convert query to vector representation
    query_vector = embeddings.embed_query(query)

    # Query Chroma DB with the vector representation
    results = collection.query(query_embeddings=query_vector, n_results=8)

    output = []

    # Save ids and texts to list and return them
    for ids, doc in zip(results['ids'], results['documents']):
        for i in range(len(ids)):
            value = {'ids': ids[i], 'context': doc[i]}
            output.append(value)

    print(output)
    return output

