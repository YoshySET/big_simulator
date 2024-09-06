import json
import os

from flask import Flask, render_template, request, abort, jsonify

app = Flask(__name__)

VALID_API_KEY = os.getenv('VALID_API_KEY')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/charts.html', methods=['GET'])
def charts():
    return render_template('charts.html')


@app.route('/tables.html', methods=['GET'])
def tables():
    return render_template('tables.html')


@app.route('/post-json-data', methods=['POST'])
def post_json_data():
    api_key = request.headers.get('x-api-key')
    if api_key != VALID_API_KEY:
        abort(401, description="Invalid API key")

    json_dict = {}
    try:
        json_dict = request.get_json()
        if json_dict is None:
            raise Exception("No JSON data provided")
    except Exception as e:
        print(e)

    try:
        with open("data.json", 'w') as json_file:
            json.dump(json_dict, json_file, indent=4)
    except Exception as e:
        print(e)
        abort(500, description="Failed to write JSON file")

    return jsonify({"message": "JSON data successfully saved"})


if __name__ == '__main__':
    app.run(debug=True)
