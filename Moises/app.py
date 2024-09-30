import time

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from controller.author_controller import AuthorController
from controller.classified_text_controller import ClassifiedController
from controller.chroma_controller import ChromaController
from controller.keyword_controller import KeywordController
from controller.reference_controller import ReferenceController
from controller.research_controller import ResearchController
from controller.topic_controller import TopicController

from chroma.read_from_chroma_script import get_data

app = Flask(__name__)
CORS(app)


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


"""
===============================
            Chroma
===============================
"""


@app.route('/chroma', methods=['POST'])
def get_chroma_record():
    if request.method != 'POST':
        return jsonify("Method is not allowed"), 405
    else:
        return ChromaController().getChromaResult(request.json)

"""
===============================
            Tweet
===============================
"""


@app.route('/classified', methods=['GET'])
def get_all_texts():
    if request.method != 'GET':
        return jsonify("Method is not allowed"), 405
    else:
        return ClassifiedController().getAllTexts()

@app.route('/classified/count', methods=['GET'])
def get_text_count():
    if request.method != 'GET':
        return jsonify("Method is not allowed"), 405
    else:
        return ClassifiedController().getTextCount()
@app.route('/classified/page', methods=['GET'])
def get_texts_by_page():
    if request.method != 'GET':
        return jsonify("Method is not allowed"), 405
    else:
        try:
            page = request.args.get('page')
            amt = request.args.get('amt')
            if not page or not amt:
                return jsonify("Missing 'page' or 'amt' parameter"), 400
            try:
                data = {
                    'page': int(page),
                    'amt': int(amt)
                }
            except ValueError:
                return jsonify("Invalid 'page' or 'amt' parameter. Must be integers."), 400
            return ClassifiedController().getTextsByPage(data)
        except Exception as e:
            print("Error processing request:", e)
            return jsonify("Invalid JSON data provided"), 404

@app.route('/classified/<text_id>', methods=['GET', 'POST'])
def get_texts_by_id(text_id):
    if request.method != 'GET':
        return jsonify("Method is not allowed"), 405
    else:
        return ClassifiedController().getTextsById(text_id)


if __name__ == "__main__":
    load_dotenv()
    app.run(host='0.0.0.0', debug=True)
