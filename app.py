from flask import Flask , jsonify, request
from flask_cors import CORS
from chatbottf import response_to_chat
app = Flask(__name__)
CORS(app)

@app.route("/chatbot",methods=["POST"])
def chatbot():
    question = request.json["question"]
    response = response_to_chat(question) 
    return jsonify(answer=response)   
