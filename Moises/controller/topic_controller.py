from flask import jsonify
from Moises.model.topic import TopicDAO


def validate_json(json):
    if 'topic' not in json:
        return None
    else:
        return "Valid"


class TopicController:
    @staticmethod
    def build_topic_dict(elements):
        result = {
            "tid": elements[0],
            "topic": elements[1]
        }
        return result

    """
    ===========================
                GET
    ===========================
    """

    def getAllTopics(self):
        dao = TopicDAO()
        topic_list = dao.getAllTopics()
        topic = [self.build_topic_dict(row) for row in topic_list]
        return jsonify(topic), 200

    def getTopicById(self, tid):
        dao = TopicDAO()
        topic_result = dao.getTopicById(tid)
        if not topic_result:
            return jsonify(f"Topic with id '{tid}' was not found"), 404
        topic = self.build_topic_dict(topic_result)
        return jsonify(topic), 200

    """
    ============================
                POST
    ============================
    """
    def createTopic(self, json):
        valid = validate_json(json)

        if not valid:
            return jsonify(f"Could not create topic. Missing attributes."), 400

        dao = TopicDAO()
        topic = json.get('topic')
        if not topic:
            return jsonify("Topic is missing"), 400

        tid = dao.createTopic(topic)
        if not tid:
            return jsonify("Topic could not be created"), 400

        topic_dict = self.build_topic_dict([tid, topic])
        return jsonify(topic_dict), 200

    """
    ===========================
                PUT
    ===========================
    """

    def updateTopic(self, tid, json):

        if not tid.isnumeric():
            return jsonify(f"'{tid}' is not a valid input"), 400

        valid = validate_json(json)
        dao = TopicDAO()
        get_id = dao.getTopicById(tid)

        if not valid:
            return jsonify(f"Could not update topic. Missing attributes."), 400

        elif not get_id:
            return jsonify(f"Topic with id '{tid}' was not found"), 404

        else:
            dao = TopicDAO()
            topic = (tid, json['topic'])
            dao.updateTopic(topic[0], topic[1])
            topic_dict = self.build_topic_dict(topic)
            return jsonify(topic_dict), 200

    """
    ==============================
                DELETE
    ==============================
    """
