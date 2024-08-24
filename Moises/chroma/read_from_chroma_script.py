from Moises.chroma.chromadb_init import get_db


def get_data(text=None):
    # Initialize Chroma DB client
    client, collection, embeddings = get_db()

    # Get user input
    if text is None:
        query = input("Enter your query: ")
    else:
        query = text['text']

    # Convert query to vector representation
    query_vector = embeddings.embed_query(query)

    # Query Chroma DB with the vector representation
    results = collection.query(query_embeddings=query_vector, n_results=5)

    output = []

    # Save ids and texts to list and return them
    for ids, doc in zip(results['ids'], results['documents']):
        for i in range(len(ids)):
            value = {'title': ids[i], 'context': doc[i]}
            output.append(value)

    print(output)
    return output

