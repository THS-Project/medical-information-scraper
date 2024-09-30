from Moises.model.db import Database
import psycopg2


class ClassifiedDAO:
    def __init__(self):
        self.db = Database()

    """
    ===========================
                GET
    ===========================
    """

    def getAllTexts(self):
        cur = self.db.connection.cursor()
        query = """SELECT text_id, t_context, health_classification, misinformation_classification
                    FROM classified_text"""
        cur.execute(query)
        author_list = [row for row in cur]
        return author_list

    def getTextCount(self):
        cur = self.db.connection.cursor()
        query = """SELECT count(*)
                            FROM classified_text"""
        cur.execute(query)
        total_count = cur.fetchone()[0]
        return total_count

    def getTextById(self, text_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT text_id, t_context, health_classification, misinformation_classification
                    FROM classified_text WHERE text_id = %s"""
            cur.execute(query, (text_id,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getTextById", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def getTextsByPage(self, page, amt):
        cur = self.db.connection.cursor()
        off = (page - 1) * amt
        query = """SELECT text_id, t_context, health_classification, misinformation_classification
                    FROM classified_text 
                    OFFSET %s
                    LIMIT %s"""
        cur.execute(query, (off, amt))
        author_list = [row for row in cur]
        return author_list