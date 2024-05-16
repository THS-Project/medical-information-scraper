from flask import jsonify
from Moises.model.keyword import KeywordDAO

def validate_json(json):
    if 'keyword' not in json:
        return None
    else:
        return "Valid"

class KeywordController:
    @staticmethod
    def build_keyword_dict(elements):
        result = {"kid": elements[0],
                  "keyword": elements[1]
                  }
        return result

    """
    ===========================
                GET
    ===========================
    """

    def getAllKeywords(self):
        dao = KeywordDAO()
        keyword_list = dao.getAllKeywords()
        keyword = [self.build_keyword_dict(row) for row in keyword_list]
        return jsonify(keyword), 200

    def getKeywordById(self, kid):
        dao = KeywordDAO()
        keyword_result = dao.getKeywordById(kid)
        if not keyword_result:
            return jsonify(f"Keyword with id '{kid}' was not found"), 404
        keyword = self.build_keyword_dict(keyword_result)
        return jsonify(keyword), 200

    """
    ============================
                POST
    ============================
    """

    # def createKeyword(self, json):

    #     valid = validate_json(json)

    #     if not valid:
    #         return jsonify(f"Could not create keyword. Missing attributes."), 400

    #     dao = KeywordDAO()
    #     keyword = (json['keyword'])
    #     kid = dao.createKeyword(keyword[0])
    #     if not kid:
    #         return jsonify("Keyword could not be created"), 400
    #     keyword_dict = self.build_keyword_dict(kid, keyword)
    #     return jsonify(keyword_dict), 200

    def createKeyword(self, json):
        valid = validate_json(json)

        if not valid:
            return jsonify(f"Could not create keyword. Missing attributes."), 400

        dao = KeywordDAO()
        keyword = json.get('keyword')
        if not keyword:
            return jsonify("Keyword is missing"), 400
        
        kid = dao.createKeyword(keyword)
        if not kid:
            return jsonify("Keyword could not be created"), 400
        
        keyword_dict = self.build_keyword_dict([kid, keyword])
        return jsonify(keyword_dict), 200
        

    """
    ===========================
                PUT
    ===========================
    """

    def updateKeyword(self, kid, json):

        if not kid.isnumeric():
            return jsonify(f"'{kid}' is not a valid input"), 400

        valid = validate_json(json)
        dao = KeywordDAO()
        get_id = dao.getKeywordById(kid)

        if not valid:
            return jsonify(f"Could not update keyword. Missing attributes."), 400

        elif not get_id:
            return jsonify(f"Keyword with id '{kid}' was not found"), 404

        else:
            dao = KeywordDAO()
            keyword = (kid, json['keyword'])
            dao.updateKeyword(keyword[0], keyword[1])
            keyword_dict = self.build_keyword_dict(keyword)
            return jsonify(keyword_dict), 200

    """
    ==============================
                DELETE
    ==============================
    """

    def deleteKeyword(self, kid):
        if not kid.isnumeric():
            return jsonify(f"'{kid}' is not a valid input"), 400

        dao = KeywordDAO()
        get_id = dao.getKeywordById(kid)

        if not get_id:
            return jsonify(f"Keyword with id '{kid}' was not found"), 404

        else:
            dao = KeywordDAO()
            removed = dao.deleteKeyword(kid)
            if not removed:
                return jsonify("Error deleting keyword"), 400
            else:
                return jsonify(f"Deleted keyword with id: {kid}"), 200
