from Moises.model.db import Database

class ResearchDAO:
    def __init__(self):
        self.db = Database()

    def getAllResearch(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM research"""
        cur.execute(query)
        research_list = [row for row in cur]
        return research_list