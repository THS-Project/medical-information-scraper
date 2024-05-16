import json
from Moises.model.db import Database
from Moises.model.author import AuthorDAO
from Moises.model.keyword import KeywordDAO
from Moises.model.research import ResearchDAO
from Moises.model.topic import TopicDAO

class DataInsert:

    def __init__(self):
        self.db = Database()

    def insert_data(self, filepath):
        cur = self.db.connection.cursor()

        # Ensure the file is a JSON file
        if not filepath.lower().endswith('.json'):
            raise ValueError("File must be a JSON file.")

        # Open and load the JSON
        with open(filepath, 'r') as f:
            data = json.load(f)

        for record in data:
            # edge cases
            doi = record.get('doi')
            title = record.get('title')
            authors = record.get('authors', [])

            # if doi, title, and authors are empty, reject json
            if not doi or not title or not authors:
                print(f"Missing required field (DOI, Title, or Authors) in JSON. JSON rejected.")
                return

            # check if doi already exists in the database, if it does, reject json
            cur.execute("""SELECT rid from research WHERE doi = %s""", (doi,))
            existing_doi = cur.fetchone()

            if existing_doi:
                print(f"DOI '{doi}' already exists in the database. JSON rejected.")
                return

            context = record.get('context')
            reference_list = record.get('reference', [])
            fullpaper = record.get('fullpaper', False)
            keywords = record.get('keywords', [])
            topics = record.get('topics', [])
            chunks = record.get('chunks', [])

            """
            ===============================
                        Research
            ===============================
            """
            research_dao = ResearchDAO()
            rid = research_dao.createResearch(title, context, doi, fullpaper)

            """
            ===============================
                        Authors
            ===============================
            """
            for author in authors:
                # "Firstname Lastname"
                fname, lname = author.split(' ', 1)

                author_dao = AuthorDAO()
                aid = author_dao.createAuthor(fname, lname)

                cur.execute("""INSERT INTO partOf (aid, rid) VALUES (%s, %s)""", (aid, rid))

            """
            ===============================
                        Keywords
            ===============================
            """
            for keyword in keywords:
                keyword_dao = KeywordDAO()
                kid = keyword_dao.createKeyword((keyword,))

                cur.execute("""INSERT INTO contains (kid, rid) VALUES (%s, %s)""", (kid, rid))

            """
            ===============================
                        Topics
            ===============================
            """
            for topic in topics:
                topic_dao = TopicDAO()
                topic_dao.createTopic((topic,))

                cur.execute("""INSERT INTO has (tid, rid) VALUES ((SELECT tid FROM topic WHERE topic = %s), %s);""", (topic, rid))

            """
            ===============================
                        References
            ===============================
            """
            reference_ids = []
            for reference in reference_list:
                cur.execute("""INSERT INTO reference (reference) VALUES (%s) RETURNING ref_id""", (reference,))
                ref_id = cur.fetchone()[0]
                reference_ids.append(ref_id)

            """
            ===============================
                        Research-Reference Relationship
            ===============================
            """
            for ref_id in reference_ids:
                cur.execute("""INSERT INTO research_reference (rid, ref_id) VALUES (%s, %s)""", (rid, ref_id))

            """
            ===============================
                        Chunks
            ===============================
            """
            for chunk in chunks:
                cid = chunk.get('cid')
                chunk_text = chunk.get('chunk')

                cur.execute("""INSERT INTO chunks (cid, rid, chunk) VALUES (%s, %s, %s)""", (cid, rid, chunk_text))

        self.db.connection.commit()
        cur.close()

        print(f"Data from {filepath} successfully added into database")

# Usage example
data_insert = DataInsert()
data_insert.insert_data("test_data.json")
