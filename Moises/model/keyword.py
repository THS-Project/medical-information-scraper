from Moises.model.db import Database
import psycopg2

class KeywordDAO:
    def __init__(self):
        self.db = Database()

    """
    ===========================
                GET
    ===========================
    """

    def getAllKeywords(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM keyword"""
        cur.execute(query)
        keyword_list = [row for row in cur]
        return keyword_list

    def getKeywordById(self, kid):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT * FROM keyword WHERE kid = %s"""
            cur.execute(query, (kid,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getKeywordById", error)
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

    def createKeyword(self, keyword):
        try:
            cur = self.db.connection.cursor()

            # check if keyword already exists
            query_check = """SELECT kid from keyword where keyword = %s"""
            cur.execute(query_check, (keyword, ))
            existing_keyword = cur.fetchone()

            # if keyword already exists
            if existing_keyword:
                print(f"Keyword already exists with kid: {existing_keyword[0]}")
                return existing_keyword[0]

            # if keyword does not exist
            query = """INSERT INTO keyword(kid, keyword)
                        VALUES(DEFAULT, %s) RETURNING kid"""
            query_values = (keyword,)
            cur.execute(query, query_values)
            self.db.connection.commit()
            kid = cur.fetchone()
            return kid



        except(Exception, psycopg2.Error) as error:
            print("Error executing createKeyword", error)
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

    def updateKeyword(self, kid, keyword):
        try:
            cur = self.db.connection.cursor()
            query = """UPDATE keyword set keyword = %s
                        WHERE kid = %s"""
            query_values = (keyword, kid)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing updateKeyword", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()

    """
    ==============================
                DELETE
    ==============================
    """

    def deleteKeyword(self, kid):
        try:
            cur = self.db.connection.cursor()
            query = """DELETE FROM keyword WHERE kid = %s"""
            query_values = (kid, )
            cur.execute(query, query_values)
            row_count = cur.rowcount
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing deleteKeyword", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()
                return row_count != 0
