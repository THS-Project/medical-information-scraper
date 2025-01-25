from flask import jsonify
from Moises.model.reference import ReferenceDAO


def validate_json(json):
    if 'reference' not in json:
        return None
    else:
        return "Valid"


class ReferenceController:
    @staticmethod
    def build_reference_dict(elements):
        result = {
            "ref_id": elements[0],
            "reference": elements[1]
        }
        return result

    """
    ===========================
                GET
    ===========================
    """

    def getAllReferences(self):
        dao = ReferenceDAO()
        reference_list = dao.getAllReferences()
        reference = [self.build_reference_dict(row) for row in reference_list]
        return jsonify(reference), 200

    def getReferenceById(self, ref_id):
        dao = ReferenceDAO()
        reference_result = dao.getReferenceById(ref_id)
        if not reference_result:
            return jsonify(f"Reference with id '{ref_id}' was not found"), 404
        reference = self.build_reference_dict(reference_result)
        return jsonify(reference), 200

    """
    ============================
                POST
    ============================
    """
    def createReference(self, json):
        valid = validate_json(json)

        if not valid:
            return jsonify(f"Could not create reference. Missing attributes."), 400

        dao = ReferenceDAO()
        reference = json.get('reference')
        if not reference:
            return jsonify("Reference is missing"), 400

        ref_id = dao.createReference(reference)
        if not ref_id:
            return jsonify("Reference could not be created"), 400

        reference_dict = self.build_reference_dict([ref_id, reference])
        return jsonify(reference_dict), 200

    def createReferenceList(self, references: list):
        dao = ReferenceDAO()
        reference = dao.getReferenceByList(references)

        output = [ref[0] for ref in reference] if reference else []
        listReference = [ref[1] for ref in reference] if reference else []
        new_elements = list(set(references) - set(listReference)) if reference else references

        for element in new_elements:
            if element in listReference:
                continue

            listReference.append(element)
            dao = ReferenceDAO()
            ref_id = dao.createReference(element)
            output.append(ref_id[0])
        return output



    """
    ===========================
                PUT
    ===========================
    """

    def updateReference(self, ref_id, json):

        if not ref_id.isnumeric():
            return jsonify(f"'{ref_id}' is not a valid input"), 400

        valid = validate_json(json)
        dao = ReferenceDAO()
        get_id = dao.getReferenceById(ref_id)

        if not valid:
            return jsonify(f"Could not update reference. Missing attributes."), 400

        elif not get_id:
            return jsonify(f"Reference with id '{ref_id}' was not found"), 404

        else:
            dao = ReferenceDAO()
            reference = (ref_id, json['reference'])
            dao.updateReference(reference[0], reference[1])
            reference_dict = self.build_reference_dict(reference)
            return jsonify(reference_dict), 200

    """
    ==============================
                DELETE
    ==============================
    """
