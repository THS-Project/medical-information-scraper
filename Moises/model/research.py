from Moises.model.db import Database
import psycopg2


class ResearchDAO:
    def __init__(self):
        self.db = Database()

    """
    ===========================
                GET
    ===========================
    """

    def getAllResearch(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM research"""
        cur.execute(query)
        research_list = [row for row in cur]
        return research_list

    def getResearchById(self, rid):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT * FROM research WHERE rid = %s"""
            cur.execute(query, (rid,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getResearchById", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    """
    ============================
                POST
    ============================
    """

    def createResearch(self, title, context, doi, reference, fullpaper):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT * FROM research WHERE rid = %s"""
            cur.execute(query, (id,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getResearchById", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result
