from Moises.create_log import log
from Moises.chroma.chromadb_init import get_db

import json
import os
import uuid

from langchain.text_splitter import RecursiveCharacterTextSplitter


def chroma_write():
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=1000,
        chunk_overlap=100)

    # Initialize Chroma DB client
    client, collection, embeddings = get_db()

    # process each JSON in the /json_management directory
    directory = 'json_management/scraped_json'
    file_counter = 0
    for filename in os.listdir(directory):

        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as json_file:
                data = json.load(json_file)
                context_value = data.get('context')

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

                if len(ids) < 1:
                    log(f'Failed to embed file #{file_counter}')
                    continue

                collection.add(
                    embeddings=embeddings_list,
                    documents=documents_list,
                    ids=ids
                )

                data['chunk_id'] = ids
                data['chunks'] = chunks

                with open(os.path.join(directory, filename), 'w') as json_file:
                    json.dump(data, json_file)

        file_counter += 1
        if file_counter % 50 == 0:
            log(f'{file_counter} files processed')

    log('Finished processing files')
