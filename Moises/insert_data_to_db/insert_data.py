import json
import os
import shutil
from Moises.model.db import Database
from Moises.model.author import AuthorDAO
from Moises.model.keyword import KeywordDAO
from Moises.model.research import ResearchDAO
from Moises.model.topic import TopicDAO

class DataInsert:

    def __init__(self):
        self.db = Database()
        self.backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "processed_json")  # Define backup directory


    # Loops through a directory and calls insert_data for each JSON file.
    def insert_data_from_directory(self):
        base_path = os.path.dirname(os.path.abspath(__file__))  # Get script directory
        json_dir = os.path.join(base_path, "..", "scraped_json")

        if not os.path.isdir(json_dir):
            raise ValueError(f"{json_dir} is not a valid directory.")

        for filename in os.listdir(json_dir):
            filepath = os.path.join(json_dir, filename)
            if filepath.lower().endswith('.json'):
                self.insert_data(filepath)

                # Move file to processed_json directory after processing
                shutil.move(filepath, os.path.join(self.backup_dir, filename))

        print(f"Finished processing files.")

    def insert_data(self, filepath):
        cur = self.db.connection.cursor()

        # Ensure the file is a JSON file
        if not filepath.lower().endswith('.json'):
            raise ValueError("File must be a JSON file.")

        # Open and load the JSON
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Extract data from JSON
        doi = data.get('doi')
        if isinstance(doi, list):
            doi = doi[0]
        title = data.get('title')
        authors = data.get('authors', [])

        # If essential fields are missing, reject JSON
        if not doi or not title or not authors:
            print(f"Missing required field (DOI, Title, or Authors) in JSON. JSON rejected.")
            return

        # Check if DOI already exists in the database
        cur.execute("""SELECT rid FROM research WHERE doi = %s""", (doi,))
        existing_doi = cur.fetchone()

        if existing_doi:
            print(f"DOI '{doi}' already exists in the database. JSON rejected.")
            return

        # Extract additional fields
        context = data.get('context')
        reference_list = data.get('references', [])
        fullpaper = data.get('isFullpaper', False)
        keywords = data.get('keywords', [])
        topic = data.get('term')
        chunk_ids = data.get('chunk_id', [])
        chunks = data.get('chunks', [])

        # Create research entry
        research_dao = ResearchDAO()
        rid = research_dao.createResearch(title, context, doi, fullpaper)

        # Insert authors
        for author in authors:
            fname, lname = author.split(' ', 1)
            author_dao = AuthorDAO()
            aid = author_dao.createAuthor(fname, lname)
            cur.execute("""INSERT INTO partOf (aid, rid) VALUES (%s, %s)""", (aid, rid))

        # Insert keywords
        for keyword in keywords:
            keyword_dao = KeywordDAO()
            kid = keyword_dao.createKeyword((keyword,))
            cur.execute("""INSERT INTO contains (kid, rid) VALUES (%s, %s)""", (kid, rid))

        # Insert topic
        topic_dao = TopicDAO()
        topic_dao.createTopic((topic,))
        cur.execute("""INSERT INTO has (tid, rid) VALUES ((SELECT tid FROM topic WHERE topic = %s), %s);""", (topic, rid))

        # Insert references
        reference_ids = []
        for reference in reference_list:
            cur.execute("""INSERT INTO reference (reference) VALUES (%s) RETURNING ref_id""", (reference,))
            ref_id = cur.fetchone()[0]
            reference_ids.append(ref_id)

        # Establish research-reference relationship
        for ref_id in reference_ids:
            cur.execute("""INSERT INTO research_reference (rid, ref_id) VALUES (%s, %s)""", (rid, ref_id))

        # Insert chunks
        for i, chunk in enumerate(chunks):
            cid = chunk_ids[i]  # Get corresponding chunk_id
            cur.execute("""INSERT INTO chunks (cid, rid, chunk) VALUES (%s, %s, %s)""", (cid, rid, chunk))

        self.db.connection.commit()
        cur.close()


# Usage example
data_insert = DataInsert()
data_insert.insert_data_from_directory()
