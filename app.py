import json
import os
import random

from flask import Flask, render_template, request, abort, jsonify

app = Flask(__name__)

VALID_API_KEY = os.getenv('VALID_API_KEY')
data_json_path = "data.json"
ad_list_json_path = "ad_list.json"
is_localhost = "false"


# context_processorを使ってテンプレート共通の変数を定義
@app.context_processor
def inject_common_variables():
    return {
        'is_localhost': os.getenv('isLocalhost')
    }


@app.route('/', methods=['GET'])
def index():
    # 本番環境起動の場合のみ広告データ読み込み
    ad_list = []
    if os.getenv('isLocalhost') != "true":
        with open(ad_list_json_path, "r", encoding="utf-8") as json_file:
            ad_list_data = json.load(json_file)
        ad_list = random.sample(ad_list_data["adList"], 2)

    with open(data_json_path, "r", encoding="utf-8") as json_file:
        big_data = json.load(json_file)

    max_vote = 0.00
    for name in ["big", "megaBIG", "100Big", "big1000", "miniBig"]:
        now_vote = float(big_data[name]["nowVote"].replace(",", ""))
        big_data[name]["nowVoteFloat"] = now_vote
        max_vote = now_vote if max_vote < now_vote else max_vote

    return render_template('index.html', big_data=big_data, max_vote=max_vote, ad_list=ad_list)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')


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
        with open(data_json_path, 'w') as json_file:
            json.dump(json_dict, json_file, indent=4)
    except Exception as e:
        print(e)
        abort(500, description="Failed to write JSON file")

    return jsonify({"message": "JSON data successfully saved"})


if __name__ == '__main__':
    os.environ['isLocalhost'] = "true"
    app.run(debug=True)
