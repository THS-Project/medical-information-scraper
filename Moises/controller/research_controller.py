from flask import jsonify
from Moises.model.research import ResearchDAO


class ResearchController:
    @staticmethod
    def build_research_dict(elements):
        result = {"rid": elements[0],
                  "title": elements[1],
                  "context": elements[2],
                  "doi": elements[3],
                  "reference": elements[4],
                  "fullpaper": elements[5]
                  }
        return result

    """
    ===========================
                GET
    ===========================
    """

    def getAllResearchs(self):
        dao = ResearchDAO()
        research_list = dao.getAllResearch()
        research = [self.build_research_dict(row) for row in research_list]
        return jsonify(research), 400

    def getResearchById(self, rid):
        dao = ResearchDAO()
        research_result = dao.getResearchById(rid)
        if not research_result:
            return jsonify(f"Research with id '{rid}' does not exist"), 404
        research = self.build_research_dict(research_result)
        return jsonify(research), 400

    """
    ============================
                POST
    ============================
    """

    def createResearch(self, json):
        dao = ResearchDAO()
        research = (json['title'], json['context'], json['doi'], json['reference'], json['fullpaper'])
        rid = dao.createResearch(research[0], research[1], research[2], research[3], research[4])
        if not rid:
            return jsonify("Research could not be created"), 400
        research_dict = self.build_research_dict((rid) + research)
        return jsonify(research_dict), 400

    """
    ===========================
                PUT
    ===========================
    """

    def getAllResearchs(self):
        dao = ResearchDAO()
        research_list = dao.getAllResearch()
        research = [self.build_research_dict(row) for row in research_list]
        return jsonify(research), 400
