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

    def getAllTexts(self, tmid: str, dtype: int):
        cur = self.db.connection.cursor()
        query = """SELECT T.textid, T.context
                    FROM llm.texts as T NATURAL INNER JOIN llm.validation_data as V INNER JOIN llm.trained_model as M
                    ON V.seed_num = M.seed_num
                    WHERE tmid = %s AND dtype = %s"""
        cur.execute(query, (tmid, dtype))
        texts_list = [row for row in cur]
        return texts_list

    def getTextById(self, text_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT textid, context
                    FROM llm.texts WHERE textid = %s"""
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

    def getModelPath(self, model_id: str):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT pathname
                    FROM llm.trained_model WHERE tmid = %s"""
            cur.execute(query, (model_id,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getModelPath", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result[0] if result else None

    def getTextsByPage(self, healthid: str, misinfoid: str, page, amt):
        cur = self.db.connection.cursor()
        off = (page - 1) * amt
        query = """(SELECT T.textid, T.context
                    FROM llm.texts as T NATURAL INNER JOIN llm.validation_data as V INNER JOIN llm.trained_model as M
                    ON V.seed_num = M.seed_num
                    WHERE tmid = %s AND dtype = 1)
                    UNION
                    (SELECT T.textid, T.context
                    FROM llm.texts as T NATURAL INNER JOIN llm.validation_data as V INNER JOIN llm.trained_model as M
                    ON V.seed_num = M.seed_num
                    WHERE tmid = %s AND dtype = 2)
                    ORDER BY 1
                    OFFSET %s
                    LIMIT %s"""
        cur.execute(query, (healthid, misinfoid, off, amt))
        text_list = [row for row in cur]
        return text_list