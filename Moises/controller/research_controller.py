from flask import jsonify
from Moises.model.research import ResearchDAO

class ResearchController:
    @staticmethod
    def build_research_dict(elements):
        result = { "rid": elements[0],
                   "title": elements[1],
                   "context": elements[2],
                   "doi": elements[3],
                   "reference": elements[4],
                   "fullpaper": elements[5]
        }
        return result


    def getAllResearchs(self):
        dao = ResearchDAO()
        research_list = dao.getAllResearch()
        research = [self.build_research_dict(row) for row in research_list]
        return jsonify(research), 400