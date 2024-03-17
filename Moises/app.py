from flask import Flask
from controller.research_controller import ResearchController

app = Flask(__name__)

@app.route('/')
def home_page():
    return "<p>Hello World</p>"


@app.route('/research')
def all_research():
    return ResearchController().getAllResearchs()








if __name__ == "__main__":
    app.run(debug=True)