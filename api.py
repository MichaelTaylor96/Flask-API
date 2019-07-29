import flask, json
from flask import request
import data, utils

app = flask.Flask(__name__)

# Refresh elasticsearch data on startup
utils.set_index()
utils.seed_data()

# Route each incoming request to the corresponding data function, return results

@app.route('/contact', methods=['GET'])
def home():
    args = request.args
    return data.home(args)

@app.route('/contact', methods=['POST'])
def post():
    body = json.loads(request.data)
    return data.post(body)

@app.route('/contact/<string:name>', methods=['GET'])
def get(name):
    return data.get(name)

@app.route('/contact/<string:name>', methods=['PUT'])
def put(name):
    body = json.loads(request.data)
    return data.put(name, body)

@app.route('/contact/<string:name>', methods=['DELETE'])
def delete(name):
    return data.delete(name)


if __name__ == "__main__":
    app.run()