# Ignore, this is just to test chroma connection and specific cases

import chromadb
from Moises.chroma import config

chroma_instance = chromadb.PersistentClient(path='../chroma'+config.db_name)
collection = chroma_instance.get_collection(name=config.collection_name)
print(chroma_instance)
print(collection)

def delete_chunks(chunk_ids):

    for chunk_id in chunk_ids:
        specific_chunk = collection.get(chunk_id)

        if specific_chunk is not None and any(specific_chunk.values()):
            collection.delete(chunk_id)
            print(f"Chunk with ID '{chunk_id}' was deleted.")

        else:
            print(f"Chunk with ID '{chunk_id}' not found in collection.")

    print(collection.count())


def check_if_chunk_exists(chunk_ids):
    for chunk_id in chunk_ids:
        specific_chunk = collection.get(chunk_id)
        if specific_chunk is not None and any(specific_chunk.values()):
            print(specific_chunk)

        else:
            print(f"Chunk with ID '{chunk_id}' not found in collection.")


#chunk_ids = ["d25f9c98-92e9-4c38-951c-1dcc6c3af625", "66c10644-eae5-4ebd-af56-b2aac8eb7bc0", "e59d5427-cc51-4f1e-9987-f4d03a93cf93", "12a5058f-b814-447b-a389-eba7e3b0ccd4", "a1d10242-f3b4-4bac-9dcf-e42b4f620d1c", "496c32ac-2163-4565-96a8-f0117dc621c4", "60ab584a-739b-45bd-bb23-667031861bdd", "cfe3a11c-e7d2-4d4f-b92d-8ac0069e22d3", "b0932f70-e46f-4548-9f8d-5a4e1abf3163", "3500cd66-43dd-4f6f-a419-72102f6a7be2", "3426da11-f0fd-473e-bdf3-441f667bd20b", "722f2ed7-65f7-45b2-926c-3675cfda3ec3", "bc51b201-aa7c-4bc0-b4f4-28cd8045f36f", "a98054ba-7737-409f-ace2-f67493f78983", "c25839b3-12b6-4736-888f-29a44116243f", "7ee72a56-6209-4315-868e-a70adf164a91", "76cfd649-f473-4b97-a7a3-8d9b02c4b935", "37cb0e95-7e19-4e75-939a-a506d83583d4", "cd0e45fa-e898-4658-b7a7-2c0276115f0a", "19d7ce7a-3b9e-436f-899b-33dab875e6f0", "f9945fb5-2ed6-48f3-91cf-5835a4297e48", "9031ec40-1957-4106-8291-87925adfd2e3", "bf998411-f832-4dde-9012-5c44bbc830fb", "4385900f-44d0-4b16-b3d9-7cb0dd182dcc", "bd1aea30-1841-4f5d-9794-81b21e9bb2af", "1fb1f3b1-d889-4966-9e35-832075470a52", "72299663-7824-4d40-854c-acac4a856680", "ec973138-69b6-449d-a4c3-0fd5220f1399", "814fd666-5d31-4c17-863b-7b34400001b9", "4ac705ad-2bc3-41d7-b551-b4d60204ac4d", "320c368e-c153-414d-a578-27ad2849756e", "410d99df-5992-4644-99e5-72dc6f870fee", "b4fa4308-288e-401c-a77c-e37d212f4b37"]
# chunk_ids = ["0ea34575-e309-4ac8-8264-688c72db42ca"]
# check_if_chunk_exists(chunk_ids)
#delete_chunks(chunk_ids)
# print(collection.count())


