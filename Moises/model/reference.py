from Moises.model.db import Database
import psycopg2

class ReferenceDAO:
    def __init__(self):
        self.db = Database()

    """
    ===========================
                GET
    ===========================
    """

    def getAllReferences(self):
        cur = self.db.connection.cursor()
        query = """SELECT * FROM reference"""
        cur.execute(query)
        reference_list = [row for row in cur]
        return reference_list

    def getReferenceById(self, ref_id):
        try:
            cur = self.db.connection.cursor()
            query = """SELECT * FROM reference WHERE ref_id = %s"""
            cur.execute(query, (ref_id,))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getReferenceById", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchone()
                cur.close()
                self.db.close()
                return result

    def getReferenceByList(self, references: list):
        try:
            cur = self.db.connection.cursor()
            query = f"""SELECT * FROM reference WHERE reference in ({','.join(['%s'] * len(references))})"""
            cur.execute(query, tuple(references))
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing getReferenceByList", error)
            self.db.connection = None

        finally:
            if self.db.connection is not None:
                result = cur.fetchall()
                cur.close()
                self.db.close()
                return result


    """
    ============================
                POST
    ============================
    """

    def createReference(self, reference):
        try:
            cur = self.db.connection.cursor()

            # check if reference already exists
            query_check = """SELECT ref_id from reference where reference = %s"""
            cur.execute(query_check, (reference, ))
            existing_reference = cur.fetchone()

            # if reference already exists
            if existing_reference:
                print(f"Reference already exists with ref_id: {existing_reference[0]}")
                return existing_reference[0]

            # if reference does not exist
            query = """INSERT INTO reference(ref_id, reference)
                        VALUES(DEFAULT, %s) RETURNING ref_id"""
            query_values = (reference,)
            cur.execute(query, query_values)
            self.db.connection.commit()
            ref_id = cur.fetchone()
            return ref_id

        except(Exception, psycopg2.Error) as error:
            print("Error executing createReference", error)
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

    def updateReference(self, ref_id, reference):
        try:
            cur = self.db.connection.cursor()
            query = """UPDATE reference set reference = %s
                        WHERE ref_id = %s"""
            query_values = (reference, ref_id)
            cur.execute(query, query_values)
            self.db.connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Error executing updateReference", error)
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
