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

            # check if research already exists
            query_check = """SELECT rid from research where title = %s AND context = %s
             AND doi = %s AND fullpaper = %s"""
            cur.execute(query_check, (title, context, doi, fullpaper))

            # if another research has the same doi
            query_check = """SELECT rid FROM research WHERE doi = %s"""
            cur.execute(query_check, (doi,))


            existing_research = cur.fetchone()

            # if research already exists
            if existing_research:
                print(f"Research already exists with aid: {existing_research[0]}")
                return existing_research[0]

            # if research does not exist
            query = """INSERT INTO research(rid, title, context, doi, fullpaper)
                        VALUES(DEFAULT, %s, %s, %s, %s) RETURNING rid"""
            query_values = (title, context, doi, fullpaper)
            cur.execute(query, query_values)
            self.db.connection.commit()
            rid = cur.fetchone()
            return rid



        except(Exception, psycopg2.Error) as error:
            print("Error executing createResearch", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()

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
