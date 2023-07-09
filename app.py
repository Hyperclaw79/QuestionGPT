"""The Flask server for the Quiz Master application."""
from __future__ import annotations
from flask import Flask, request, jsonify
from gpt_client import GptClient
from models.question_formats import QT_MAPPING, Difficulty
from utils.schema_gen import to_schema

app = Flask(__name__)

gpt_client = GptClient()


@app.route("/get_question", methods=["GET", "POST"])
def get_question() -> tuple[dict[str, str], int]:
    """Endpoint for getting a question from the GPT API.

    :return: A tuple containing the response and status code.
    """
    if request.method == "GET":
        data = request.args
    else:
        data = request.get_json()
    question_type = data.get("question_type")
    difficulty = data.get("difficulty")
    topic = data.get("topic")
    instructions = data.get("instructions", "")
    question_cls = QT_MAPPING.get(question_type)
    if not question_cls:
        return jsonify({"error": "Invalid question type"}), 400
    try:
        Difficulty(difficulty)
    except ValueError:
        return jsonify({"error": "Invalid difficulty"}), 400
    if not topic:
        return jsonify({"error": "Invalid topic"}), 400
    schema = to_schema(question_cls)
    try:
        question = gpt_client.prompt(
            schema, question_type, difficulty,
            topic, instructions
        )
    except Exception as exp:  # pylint: disable=broad-except
        return jsonify({"Unkown error": str(exp)}), 500
    return jsonify(question), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
