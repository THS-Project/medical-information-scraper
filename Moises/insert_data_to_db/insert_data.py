import chromadb
import json
import nameparser
import os
import shutil
from Moises.controller.reference_controller import ReferenceController
from Moises.chroma import dbconfig
from Moises.model.db import Database
from Moises.model.author import AuthorDAO
from Moises.model.keyword import KeywordDAO
from Moises.model.research import ResearchDAO
from Moises.model.topic import TopicDAO
from Moises.model.reference import ReferenceDAO
from Moises.create_log import log


class DataInsert:

    def __init__(self):
        self.db = Database()
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.backup_dir = os.path.join(base_path, "../json_management/processed_json")
        self.rejected_dir = os.path.join(base_path, "../json_management/rejected_json")

    # Loops through scraped_json directory and calls insert_data for each JSON
    def insert_data_from_directory(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_dir = os.path.join(base_path, "../json_management/scraped_json")

        # Create directories if they do not exist
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.rejected_dir, exist_ok=True)


        if not os.path.isdir(json_dir):
            raise ValueError(f"{json_dir} is not a valid directory.")

        for filename in os.listdir(json_dir):
            filepath = os.path.join(json_dir, filename)
            if filepath.lower().endswith('.json'):
                print(f"---------Processing '{filename}'---------")
                try:
                    self.insert_data(filepath)
                    # If insert_data does not raise an exception, move file to processed_json
                    shutil.move(filepath, os.path.join(self.backup_dir, filename))
                except ValueError as e:
                    print(f"Error processing file '{filename}': {e}")
                    # Move rejected file to rejected_json directory
                    shutil.move(filepath, os.path.join(self.rejected_dir, filename))

        log("Finished processing files to Postgres.")

    def insert_data(self, filepath):
        # Ensure the file is a JSON file
        if not filepath.lower().endswith('.json'):
            raise ValueError("File must be a JSON file.")

        # Open and load the JSON
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Extract records from JSON
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

        # Edge cases to reject JSON
        if not doi or not title or not authors:
            self.reject_json("Missing required field (doi, title, or authors) in JSON.", chunk_ids)
            raise ValueError("Missing required field (doi, title, or authors) in JSON.")

        with self.db.connection.cursor() as cur:
            # Check if DOI already exists in the database
            cur.execute("""SELECT rid FROM research WHERE doi = %s""", (doi,))
            existing_doi = cur.fetchone()
            if existing_doi:
                self.reject_json(f"DOI '{doi}' already exists in the database. JSON rejected.", chunk_ids)
                raise ValueError(f"DOI '{doi}' already exists in the database.")

            # Inserting Data to Postgres
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

            # Check if the author-research relationship already exists
            cur.execute("""SELECT 1 FROM partOf WHERE aid = %s AND rid = %s""", (aid, rid))
            if not cur.fetchone():
                # Insert research-author relationship if it doesn't exist
                cur.execute("""INSERT INTO partOf (aid, rid) VALUES (%s, %s)""", (aid, rid))

    def insert_keywords(self, keywords, rid, cur):
        # Insert keywords
        for keyword in keywords:
            keyword_dao = KeywordDAO()
            kid = keyword_dao.createKeyword((keyword,))

            # Check if the keyword-research relationship already exists
            cur.execute("""SELECT 1 FROM contains WHERE kid = %s AND rid = %s""", (kid, rid))
            if not cur.fetchone():
                # Insert research-keyword relationship if it doesn't exist
                cur.execute("""INSERT INTO contains (kid, rid) VALUES (%s, %s)""", (kid, rid))

    def insert_topic(self, topic, rid, cur):
        # Insert topic
        topic_dao = TopicDAO()
        tid = topic_dao.createTopic((topic,))

        # Check if the topic-research relationship already exists
        cur.execute("""SELECT tid FROM has NATURAL INNER JOIN topic WHERE topic = %s AND rid = %s""", (topic, rid))
        if not cur.fetchone():
            # Insert research-topic relationship if it doesn't exist
            cur.execute("""INSERT INTO has (tid, rid) VALUES (%s, %s)""", (tid, rid))

    def insert_references(self, references: list, rid: int, cur):
        if len(references) < 1:
            return
        # Insert references
        ref_ids = ReferenceController().createReferenceList(references)
        for ref_id in ref_ids:
            # Check if the research-reference relationship already exists
            cur.execute("""SELECT 1 FROM research_reference WHERE rid = %s AND ref_id = %s""", (rid, ref_id))
            if not cur.fetchone():
                # Insert research-reference relationship if it doesn't exist
                cur.execute("""INSERT INTO research_reference (rid, ref_id) VALUES (%s, %s)""", (rid, ref_id))

    def insert_chunks(self, chunk_ids, chunks, rid, cur):
        # Insert chunks
        for i, chunk in enumerate(chunks):
            cid = chunk_ids[i]  # Get corresponding chunk_id
            cur.execute("""INSERT INTO chunks (cid, rid, chunk) VALUES (%s, %s, %s)""", (cid, rid, chunk))

    # Deletes chunks from chroma
    def delete_chunks(self, chunk_ids):
        # Connect to Chroma and delete specified chunks
        chroma_instance = chromadb.PersistentClient(path=dbconfig.db_name)
        collection = chroma_instance.get_collection(name=dbconfig.collection_name)

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
