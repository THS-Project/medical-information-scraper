from flask import jsonify
from Moises.model.research import ResearchDAO


def validate_json(json):
    required_fields = ['title', 'context', 'doi', 'reference', 'fullpaper']
    if not all(field in json for field in required_fields):
        return None
    else:
        return "Valid"


class ResearchController:
    @staticmethod
    def build_research_dict(elements):
        result = {
            "rid": elements[0],
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
        return jsonify(research), 200

    def getResearchById(self, rid):
        dao = ResearchDAO()
        research_result = dao.getResearchById(rid)
        if not research_result:
            return jsonify(f"Research with id '{rid}' was not found"), 404
        research = self.build_research_dict(research_result)
        return jsonify(research), 200

    def createResearch(self, json):
        valid = validate_json(json)
        if not valid:
            return jsonify("Could not create research. Missing attributes."), 400

        dao = ResearchDAO()
        # Check if research with the same title, context, doi, and reference already exists
        existing_research = dao.getResearchByAttributes(
            json['title'], json['context'], json['doi'], json['reference']
        )
        if existing_research:
            return jsonify("Research already exists with the provided attributes"), 400

        # Create the research if it does not already exist
        research = (json['title'], json['context'], json['doi'], json['reference'], json['fullpaper'])
        rid = dao.createResearch(research[0], research[1], research[2], research[3], research[4])
        if not rid:
            return jsonify("Research could not be created"), 400
        research_dict = self.build_research_dict((rid,) + research)
        return jsonify(research_dict), 200

    def updateResearch(self, rid, json):
        if not rid.isnumeric():
            return jsonify(f"'{rid}' is not a valid input"), 400

        valid = validate_json(json)
        dao = ResearchDAO()
        get_id = dao.getResearchById(rid)

        if not valid:
            return jsonify(f"Could not update research. Missing attributes."), 400
        elif not get_id:
            return jsonify(f"Research with id '{rid}' was not found"), 404

        # Update the research
        research = (rid, json['title'], json['context'], json['doi'], json['reference'], json['fullpaper'])
        dao.updateResearch(research[0], research[1], research[2], research[3], research[4], research[5])
        research_dict = self.build_research_dict(research)
        return jsonify(research_dict), 200

    def deleteResearch(self, rid):
        if not rid.isnumeric():
            return jsonify(f"'{rid}' is not a valid input"), 400

        dao = ResearchDAO()
        get_id = dao.getResearchById(rid)

        if not get_id:
            return jsonify(f"Research with id '{rid}' was not found"), 404

        removed = dao.deleteResearch(rid)
        if not removed:
            return jsonify("Error deleting research"), 400
        else:
            return jsonify(f"Deleted research with id: {rid}"), 200
