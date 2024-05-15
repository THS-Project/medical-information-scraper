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
        try:
            cur = self.db.connection.cursor()
            query = """SELECT * FROM research"""
            cur.execute(query)
            research_list = [row for row in cur]
            return research_list

        except (Exception, psycopg2.Error) as error:
            print("Error executing getAllResearch", error)
            return []

        finally:
            if self.db.connection is not None:
                cur.close()

    def getResearchById(self, rid):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT * FROM research WHERE rid = %s"""
            cur.execute(query, (rid,))
            result = cur.fetchone()
            return result

        except (Exception, psycopg2.Error) as error:
            print("Error executing getResearchById", error)
            return None

        finally:
            if self.db.connection is not None:
                cur.close()

    """
    ============================
                POST
    ============================
    """

    def createResearch(self, title, context, doi, fullpaper):
        try:
            cur = self.db.connection.cursor()
            query = """INSERT INTO research(title, context, doi, fullpaper)
                        VALUES (%s, %s, %s, %s) RETURNING rid"""
            query_values = (title, context, doi, fullpaper)
            cur.execute(query, query_values)
            rid = cur.fetchone()[0]
            self.db.connection.commit()
            return rid

        except (Exception, psycopg2.Error) as error:
            print("Error executing createResearch", error)
            return None

        finally:
            if self.db.connection is not None:
                cur.close()

    """
    ===========================
                PUT
    ===========================
    """

    def updateResearch(self, rid, title, context, doi, fullpaper):
        try:
            cur = self.db.connection.cursor()
            query = """UPDATE research SET title = %s, context = %s, doi = %s, fullpaper = %s
                        WHERE rid = %s"""
            query_values = (title, context, doi, fullpaper, rid)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error executing updateResearch", error)

        finally:
            if self.db.connection is not None:
                cur.close()

    """
    ==============================
                DELETE
    ==============================
    """

    def deleteResearch(self, rid):
        try:
            cur = self.db.connection.cursor()
            query = """DELETE FROM research WHERE rid = %s"""
            query_values = (rid,)
            cur.execute(query, query_values)
            row_count = cur.rowcount
            self.db.connection.commit()
            return row_count != 0

        except (Exception, psycopg2.Error) as error:
            print("Error executing deleteResearch", error)
            return False

        finally:
            if self.db.connection is not None:
                cur.close()
