"""The Flask server for the Quiz Master application."""
from __future__ import annotations
from flask import Flask, request, jsonify
from gpt_client import GptClient
from models.gpt_models import UserInput
from models.question_formats import QT_MAPPING
from utils.helpers import extract_fields
from utils.schema_gen import to_schema

app = Flask(__name__)

gpt_client = GptClient()


@app.route("/get_question", methods=["GET", "POST", "OPTIONS"])
def get_question() -> tuple[dict[str, str], int]:
    """Endpoint for getting a question from the GPT API.

    :return: A tuple containing the response and status code.
    """
    if request.method == "OPTIONS":
        input_fields = extract_fields(UserInput)
        response = {
            'allowed_methods': ['GET', 'POST'],
            'parameters': {
                'GET': input_fields,
                'POST': input_fields
            }
        }
        return jsonify(response), 200
    if request.method == "GET":
        data = request.args
    else:
        data = request.get_json()
    try:  # Validate the user input
        user_input = UserInput(**data)
    except ValueError as exp:
        return jsonify({"error": str(exp)}), 400
    question_cls = QT_MAPPING.get(user_input.question_type)
    schema = to_schema(question_cls)
    try:
        question = gpt_client.prompt(schema, **data)
    except Exception as exp:  # pylint: disable=broad-except
        return jsonify({"Unkown error": str(exp)}), 500
    return jsonify(question), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
