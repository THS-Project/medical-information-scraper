from flask import Flask, request, jsonify
from controller.research_controller import ResearchController

app = Flask(__name__)

@app.route('/')
def home_page():
    return "<p>Hello World</p>"


"""
===============================
            Author
===============================
"""



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



"""
===============================
            PartOf
===============================
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
        return ResearchController().createResearch()

    else:
        return jsonify("Method is not allowed"), 405

@app.route('/research/<id>', methods=['GET', 'PUT', 'DELETE'])
def research_by_id(rid):
    if request.method == 'GET':
        return ResearchController().getResearchById(rid)

    elif request.method == 'PUT':
        return ResearchController().updateResearch(rid)

    elif request.method == 'DELETE':
        return ResearchController().deleteResearch(rid)

    else:
        return jsonify("Method is not allowed"), 405

"""
===============================
            Topic
===============================
"""



if __name__ == "__main__":
    app.run(debug=True)