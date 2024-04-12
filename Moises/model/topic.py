from Moises.model.db import Database
import psycopg2


class TopicDAO:
    def __init__(self):
        self.db = Database()

    """
    ===========================
                GET
    ===========================
    """

    def getAllTopics(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM topic"""
        cur.execute(query)
        topic_list = [row for row in cur]
        return topic_list

    def getTopicById(self, tid):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT * FROM topic WHERE tid = %s"""
            cur.execute(query, (tid,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getTopicById", error)
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

    def createTopic(self, topic):
        try:
            cur = self.db.connection.cursor()
            query = """INSERT INTO topic(tid, topic) VALUES(DEFAULT, %s) RETURNING tid"""
            query_values = (topic)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing createTopic", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                tid = cur.fetchone()
                cur.close()
                self.db.close()
                return tid


    """
    ===========================
                PUT
    ===========================
    """

    def updateTopic(self, tid, topic):
        try:
            cur = self.db.connection.cursor()
            query = """UPDATE topic set topic = %s WHERE tid = %s"""
            query_values = (topic, tid)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing updateTopic", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                cur.close()
                self.db.close()




