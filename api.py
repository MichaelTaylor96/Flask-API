import flask
from flask import request
import data

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# @app.route('/contact', methods=['GET'])
# def home():

# @app.route('/contact', methods=['POST'])
# def post():
#     body = request.data
#     return data.post(body)

@app.route('/contact/<string:name>', methods=['GET'])
def get(name):
    return data.get(name)

# @app.route('/contact/<string:name>', methods=['PUT'])
# def put(name):

# @app.route('/contact/<string:name>', methods=['DELETE'])
# def delete(name):


if __name__ == "__main__":
    app.run()