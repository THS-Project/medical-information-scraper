from Moises.model.db import Database
import psycopg2

class AuthorDAO:
    def __init__(self):
        self.db = Database()
        
    """
    ===========================
                GET
    ===========================
    """
    
    def getAllAuthor(self):
        cur = self.db.connection.cursor()
        query = """SELECT aid, fname, lname FROM author"""
        cur.execute(query)
        author_list = [row for row in cur]
        return author_list

    def getAuthorById(self, aid):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT aid, fname, lname FROM author WHERE aid = %s"""
            cur.execute(query, (aid,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getAuthorById", error)
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

    def createAuthor(self, fname, lname):
        try:
            cur = self.db.connection.cursor()
            query = """INSERT INTO author(aid, fname, lname)
                        VALUES(DEFAULT, %s, %s) RETURNING aid"""
            query_values = (fname, lname)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing createAuthor", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                aid = cur.fetchone()
                cur.close()
                self.db.close()
                return aid

    """
    ===========================
                PUT
    ===========================
    """

    def updateAuthor(self, aid, fname, lname):
        try:
            cur = self.db.connection.cursor()
            query = """UPDATE author set fname = %s, lname = %s
                        WHERE aid = %s"""
            query_values = (fname, lname, aid)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing updateAuthor", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()
