from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from util import m

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

@app.route('/postdata', methods=['POST'])
def submitFile():
    data = request.json

    status = 'OK'
    result_msg = 'Failed'
    result = 'None'

    images = data['images']
    mode = data['mode']

    result_msg, result = m.mergeImages(images, mode)

    return {'status': status, 'result_msg': result_msg, 'result': result}

if __name__ == '__main__':
    app.run(debug=False)