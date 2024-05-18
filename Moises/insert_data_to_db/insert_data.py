import json
import os
import shutil
import chromadb
import nameparser
from Moises.model.db import Database
from Moises.model.author import AuthorDAO
from Moises.model.keyword import KeywordDAO
from Moises.model.research import ResearchDAO
from Moises.model.topic import TopicDAO
from Moises.model.reference import ReferenceDAO

class DataInsert:

    def __init__(self):
        self.db = Database()
        self.backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "processed_json")


    # loops through scraped_json directory and calls insert_data for each JSON
    def insert_data_from_directory(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_dir = os.path.join(base_path, "..", "scraped_json")

        if not os.path.isdir(json_dir):
            raise ValueError(f"{json_dir} is not a valid directory.")

        for filename in os.listdir(json_dir):
            filepath = os.path.join(json_dir, filename)
            if filepath.lower().endswith('.json'):
                print(f"Processing '{filename}'")
                self.insert_data(filepath)

                # Move json to processed_json directory after inserting in db
                shutil.move(filepath, os.path.join(self.backup_dir, filename))

        print(f"Finished processing files.")


    def insert_data(self, filepath):
        #cur = self.db.connection.cursor()

        # Ensure the file is a JSON file
        if not filepath.lower().endswith('.json'):
            raise ValueError("File must be a JSON file.")

        # Open and load the JSON
        with open(filepath, 'r') as f:
            data = json.load(f)

    # ---- Extract records from JSON ----
        doi = data.get('doi')
        if isinstance(doi, list):
            doi = doi[0]

        title = data.get('title')
        authors = data.get('authors', [])
        chunk_ids = data.get('chunk_id', [])
        chunks = data.get('chunks', [])
        context = data.get('context')
        reference_list = data.get('references', [])
        fullpaper = data.get('isFullpaper', False)
        keywords = data.get('keywords', [])
        topic = data.get('term')


    #------ Edge cases to reject JSON ------

        # If doi, title and context are missing, reject JSON and delete chunks from chroma
        if not doi or not title or not authors:
            self.reject_json("Missing required field (doi, title, or authors) in JSON.", chunk_ids)

        with self.db.connection.cursor() as cur:

            # Check if DOI already exists in the database. If it does, reject JSON and delete chunks from chroma
            cur.execute("""SELECT rid FROM research WHERE doi = %s""", (doi,))
            existing_doi = cur.fetchone()
            if existing_doi:
                self.reject_json("DOI '{doi}' already exists in the database. JSON rejected.", chunk_ids)


            #-------Inserting Data to Postgres-----
            rid = self.insert_research(title, context, doi, fullpaper)
            self.insert_authors(authors, rid, cur)
            self.insert_keywords(keywords, rid, cur)
            self.insert_topic(topic, rid, cur)
            self.insert_references(reference_list, rid, cur)
            self.insert_chunks(chunk_ids, chunks, rid, cur)

        self.db.connection.commit()
        cur.close()


    def reject_json(self, reason, chunk_ids):
        # Print rejection reason and delete associated chunks
        print(f"{reason} JSON rejected.")
        self.delete_chunks(chunk_ids)

    def insert_research(self, title, context, doi, fullpaper):
        # Insert research
        research_dao = ResearchDAO()
        rid = research_dao.createResearch(title, context, doi, fullpaper)
        return rid

    def insert_authors(self, authors, rid, cur):
        # Insert authors
        for author in authors:
            fname, lname = self.parse_author_name(author)
            author_dao = AuthorDAO()
            aid = author_dao.createAuthor(fname, lname)
            # Insert research-author relationship
            cur.execute("""INSERT INTO partOf (aid, rid) VALUES (%s, %s)""", (aid, rid))

    def insert_keywords(self, keywords, rid, cur):
        # Insert keywords
        for keyword in keywords:
            keyword_dao = KeywordDAO()
            kid = keyword_dao.createKeyword((keyword,))
            # Insert research-keyword relationship
            cur.execute("""INSERT INTO contains (kid, rid) VALUES (%s, %s)""", (kid, rid))

    def insert_topic(self, topic, rid, cur):
        # Insert topic
        topic_dao = TopicDAO()
        topic_dao.createTopic((topic,))
        # Insert research-topic relationship
        cur.execute("""INSERT INTO has (tid, rid) VALUES ((SELECT tid FROM topic WHERE topic = %s), %s);""", (topic, rid))

    def insert_references(self, references, rid, cur):
        # Insert references
        for reference in references:
            reference_dao = ReferenceDAO()
            ref_id = reference_dao.createReference((reference,))
            # Insert research-reference relationship
            cur.execute("""INSERT INTO research_reference (rid, ref_id) VALUES (%s, %s)""", (rid, ref_id))

    def insert_chunks(self, chunk_ids, chunks, rid, cur):
        # Insert chunks
        for i, chunk in enumerate(chunks):
            cid = chunk_ids[i]  # Get corresponding chunk_id
            cur.execute("""INSERT INTO chunks (cid, rid, chunk) VALUES (%s, %s, %s)""", (cid, rid, chunk))

    # Deletes chunks from chroma
    def delete_chunks(self, chunk_ids):
        # Connect to Chroma and delete specified chunks
        chroma_instance = chromadb.PersistentClient(path="./chroma/db1")
        collection = chroma_instance.get_collection("collection1")

        for chunk_id in chunk_ids:
            chunk = collection.get(chunk_id)

            if chunk is not None and any(chunk.values()):
                collection.delete(chunk_id)
                print(f"Chunk with ID '{chunk_id}' was deleted from Chroma.")

            else:
                print(f"Chunk with ID '{chunk_id}' not found in Chroma.")

        print(f"Total chunks in collection: {collection.count()}")

    def parse_author_name(self, author):
        parsed_name = nameparser.HumanName(author.strip())
        names = parsed_name.as_dict()

        if 'middle' in names:
            if names['middle'].endswith('.'):
                # Middle name with a dot, treat it as part of the first name
                fname = parsed_name.first + " " + parsed_name.middle
                lname = parsed_name.last
            else:
                # Middle name without a dot, treat it as the last name
                fname = parsed_name.first
                lname = " ".join([parsed_name.middle, parsed_name.last])
        else:
            # No middle name
            fname = parsed_name.first
            lname = parsed_name.last

        # Strip leading and trailing spaces before inserting
        fname = fname.strip()
        lname = lname.strip()

        return fname, lname


data_insert = DataInsert()
data_insert.insert_data_from_directory()
