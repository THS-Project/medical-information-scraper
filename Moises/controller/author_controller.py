from flask import jsonify
from Moises.model.author import AuthorDAO

def validate_json(json):
    if 'fname' not in json or 'lname' not in json:
        return None
    else:
        return "Valid"
    

class AuthorController:
    
    @staticmethod
    def build_author_dict(elements):
        result = {'aid': elements[0],
                  'fname': elements[1],
                  'lname': elements[2]
                  }
        return result
    
    """
    ===========================
                GET
    ===========================
    """
    def getAllAuthors(self):
        dao = AuthorDAO()
        author_list = dao.getAllAuthor()
        author = [self.build_author_dict(row) for row in author_list]
        return jsonify(author), 400

    def getAuthorById(self, aid):
        dao = AuthorDAO()
        author_result = dao.getAuthorById(aid)
        if not author_result:
            return jsonify(f"Author with id '{aid}' was not found"), 404
        author = self.build_author_dict(author_result)
        return jsonify(author), 200
    
    """
    ============================
                POST
    ============================
    """
    
    def createAuthor(self, json):

        valid = validate_json(json)

        if not valid:
            return jsonify(f"Could not create author. Missing attributes."), 400

        dao = AuthorDAO()
        author = (json['fname'], json['lname'])
        aid = dao.createAuthor(author[0], author[1])
        if not aid:
            return jsonify("Author could not be created"), 400

        author_dict = self.build_author_dict(aid + author)
        return jsonify(author_dict), 200
    
    """
    ===========================
                PUT
    ===========================
    """

    def updateAuthor(self, aid, json):

        if not aid.isnumeric():
            return jsonify(f"'{aid}' is not a valid input"), 400

        valid = validate_json(json)
        dao = AuthorDAO()
        get_id = dao.getAuthorById(aid)

        if not valid:
            return jsonify(f"Could not update author. Missing attributes."), 400

        elif not get_id:
            return jsonify(f"Author with id '{aid}' was not found"), 404

        else:
            dao = AuthorDAO()
            author = (aid, json['fname'], json['lname'])
            dao.updateAuthor(author[0], author[1], author[2])
            author_dict = self.build_author_dict(author)
            return jsonify(author_dict), 200
