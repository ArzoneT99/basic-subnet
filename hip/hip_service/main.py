from flask import Flask, request, jsonify, send_from_directory
import os
import time
from client import Database, Answer
from sqlalchemy import event

qAdb = Database("sqlite:///QA.db")

app = Flask(__name__, static_folder='public')
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions = qAdb.get_unanswered_questions().all()
    questions_list = [{'id': q.id, 'label': q.label, 'type': q.type,
                       'value': q.value, 'image': q.image, 'options': q.options} for q in questions]
    return jsonify({'questions': questions_list})


@app.route('/api/answer', methods=['POST'])
def post_answer():
    answer_data = request.json
    if not answer_data or not answer_data.get('id') or not answer_data.get('answer'):
        return jsonify({"message": "Missing required fields."}), 400

    new_answer = Answer()
    new_answer.answer = answer_data.get('answer')
    new_answer.question_id = answer_data.get('id')

    qAdb.create_answer(id=new_answer.question_id, answer=new_answer.answer, question_id=new_answer.question_id)

    return jsonify({"message": "Answer added successfully."}), 201


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and app.static_folder is not None and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    elif app.static_folder is not None:
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return "Static folder is not specified."


if __name__ == '__main__':
    app.run(port=6891, debug=True)
