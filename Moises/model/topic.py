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

            # check if topic already exists
            query_check = """SELECT tid from topic where topic = %s"""
            cur.execute(query_check, (topic, ))
            existing_topic = cur.fetchone()

            # if topic already exists
            if existing_topic:
                print(f"Topic already exists with tid: {existing_topic[0]}")
                return existing_topic[0]

            # if topic does not exist
            query = """INSERT INTO topic(tid, topic)
                        VALUES(DEFAULT, %s) RETURNING tid"""
            query_values = (topic,)
            cur.execute(query, query_values)
            self.db.connection.commit()
            tid = cur.fetchone()
            return tid



        except(Exception, psycopg2.Error) as error:
            print("Error executing createTopic", error)
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

    def updateTopic(self, tid, topic):
        try:
            cur = self.db.connection.cursor()
            query = """UPDATE topic set topic = %s
                        WHERE tid = %s"""
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

    """
    ==============================
                DELETE
    ==============================
    """
