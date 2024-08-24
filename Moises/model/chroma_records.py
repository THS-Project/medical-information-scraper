from Moises.model.db import Database
import psycopg2


class ChromaDAO:
    def __init__(self):
        self.db = Database()

    """
    ===========================
                GET
    ===========================
    """

    def getChromaReferences(self, cid):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT reference
                    FROM chunks NATURAL INNER JOIN research
                    NATURAL INNER JOIN research_reference
                    NATURAL INNER JOIN reference
                    WHERE cid = %s"""
            cur.execute(query, (cid,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getChromaReferences", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result

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
