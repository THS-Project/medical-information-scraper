from flask import Flask, request, jsonify
from controller.research_controller import ResearchController
from controller.author_controller import AuthorController
from controller.topic_controller import TopicController
from controller.keyword_controller import KeywordController
from controller.reference_controller import ReferenceController




app = Flask(__name__)


@app.route('/')
def home_page():
    return "<p>Hello World</p>"


"""
===============================
            Author
===============================
"""

@app.route('/author', methods=['GET', 'POST'])
def author():
    if request.method == 'GET':
        return AuthorController().getAllAuthors()

    elif request.method == 'POST':
        return AuthorController().createAuthor(request.json)

    else:
        return jsonify("Method is not allowed"), 405


@app.route('/author/<aid>', methods=['GET', 'PUT'])
def author_by_id(aid):
    if request.method == 'GET':
        return AuthorController().getAuthorById(aid)

    elif request.method == 'PUT':
        return AuthorController().updateAuthor(aid, request.json)

    else:
        return jsonify("Method is not allowed"), 405

"""
===============================
            Chunks
===============================
"""

"""
===============================
            Contains
===============================
"""

"""
============================
            Has
============================
"""

"""
===============================
            Keyword
===============================
"""

@app.route('/keyword', methods=['GET', 'POST'])
def keyword():
    if request.method == 'GET':
        return KeywordController().getAllKeywords()

    elif request.method == 'POST':
        return KeywordController().createKeyword(request.json)

    else:
        return jsonify("Method is not allowed"), 405

@app.route('/keyword/<kid>', methods=['GET', 'PUT', 'DELETE'])
def keyword_by_id(kid):
    if request.method == 'GET':
        return KeywordController().getKeywordById(kid)

    elif request.method == 'PUT':
        return KeywordController().updateKeyword(kid, request.json)

    elif request.method == 'DELETE':
        return KeywordController().deleteKeyword(kid)

    else:
        return jsonify("Method is not allowed"), 405

"""
===============================
            PartOf
===============================
"""
"""
=================================
            Reference
=================================
"""
@app.route('/reference', methods=['GET', 'POST'])
def reference():
    if request.method == 'GET':
        return ReferenceController().getAllReferences()

    elif request.method == 'POST':
        return ReferenceController().createReference(request.json)

    else:
        return jsonify("Method is not allowed"), 405


@app.route('/reference/<ref_id>', methods=['GET', 'PUT'])
def reference_by_id(ref_id):
    if request.method == 'GET':
        return ReferenceController().getReferenceById(ref_id)

    elif request.method == 'PUT':
        return ReferenceController().updateReference(ref_id, request.json)

    else:
        return jsonify("Method is not allowed"), 405


"""
=================================
    Research_Reference 
=================================
"""


"""
=================================
            Research
=================================
"""

@app.route('/research', methods=['GET', 'POST'])
def research():
    if request.method == 'GET':
        return ResearchController().getAllResearchs()

    elif request.method == 'POST':
        return ResearchController().createResearch(request.json)

    else:
        return jsonify("Method is not allowed"), 405


@app.route('/research/<rid>', methods=['GET', 'PUT', 'DELETE'])
def research_by_id(rid):
    if request.method == 'GET':
        return ResearchController().getResearchById(rid)

    elif request.method == 'PUT':
        return ResearchController().updateResearch(rid, request.json)

    elif request.method == 'DELETE':
        return ResearchController().deleteResearch(rid)

    else:
        return jsonify("Method is not allowed"), 405


"""
===============================
            Topic
===============================
"""
@app.route('/topic', methods=['GET', 'POST'])
def topic():
    if request.method == 'GET':
        return TopicController().getAllTopics()

    elif request.method == 'POST':
        return TopicController().createTopic(request.json)

    else:
        return jsonify("Method is not allowed"), 405


@app.route('/topic/<tid>', methods=['GET', 'PUT'])
def topic_by_id(tid):
    if request.method == 'GET':
        return TopicController().getTopicById(tid)

    elif request.method == 'PUT':
        return TopicController().updateTopic(tid, request.json)

    else:
        return jsonify("Method is not allowed"), 405


if __name__ == "__main__":
    app.run(debug=True)
