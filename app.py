from flask import Flask, jsonify, request
from flask_cors import CORS
from chatbottf import response_to_chat
app = Flask(__name__)
CORS(app)


def checkquestion(question):
    if question == "daftar" or question == "pendaftaran":
        return '''
            Mungkin yang anda maksud adalah : 
            <ol>
                <li>Daftar Tes Bahasa</li>
                <li>Daftar Ujian Susulan</li>
                <li>Daftar Mahasiswa Baru</li>
                <li>Daftar SK TA/PA</li>
            </ol> 
        '''
    elif question == "ujian":
        return '''
            Mungkin yang anda maksud adalah : 
            <ol>
                <li>Ujian Semester</li>
                <li>Ujian Susulan</li>             
            </ol> 
        '''
    elif question == "jadwal":
        return '''
            Mungkin yang anda maksud adalah : 
            <ol>
                <li>Jadwal Mata Kuliah</li>
                <li>Jadwal Ujian Semester</li>
                <li>Jadwal Ujian Susulan</li>
                <li>Jadwal Sidang</li>             
            </ol> 
        '''
    elif question == "nilai":
        return '''
            Mungkin yang anda maksud adalah : 
            <ol>
                <li>Nilai Akademik</li>
                <li>Nilai Tes Bahasa</li>          
            </ol> 
        '''


checked_one_word = ["daftar", "pendaftaran", "ujian", "jadwal", "nilai"]


@app.route("/chatbot", methods=["POST"])
def chatbot():
    question = request.json["question"]
    if len(question.split(" ")) == 1 and question in checked_one_word:
        response = checkquestion(question)
    else:
        response = response_to_chat(question)
    return jsonify(answer=response)
