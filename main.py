from flask import Flask, jsonify, request
app = Flask(__name__)
from websites import Url

@app.route('/', methods=['GET'])
def main():
    return jsonify({"Message": "Welcome to the server"})


@app.route('/check/<path:url>', methods=['GET'])
def scan_url(url):
    res = request.view_args['url']
    o = Url(res)
    return jsonify(o.run())



if __name__ == '__main__':
    app.run(debug=True, port=8080)