from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from uuid import uuid4
from util import merger_v2
app = Flask(__name__)

SAVE_PATH = 'static/images/'
ALLOWED_MIME = ['image/jpeg', 'image/png']
GO_BACK_LINK = '<a href="/">Go back</a>'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/error')
def error_page():
    return render_template('error.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        mode = request.form['mode']
        rows = int(request.form['rows'])
        file_list = request.files.getlist('file')
        
        if mode == 'cs':
            if rows <= 0:
                return "<h3>Rows should bigger than 0!</h3><br>{}".format(GO_BACK_LINK)
            elif rows > len(file_list):
                return "<h3>Too many rows, sorry!</h3><br>{}".format(GO_BACK_LINK)

        dst = uuid4().hex + '.jpg'
        fs_n = []
        for f in file_list:
            if f.content_type not in ALLOWED_MIME:
                return "<h3>Please upload png & jpg only!</h3><br>{}".format(GO_BACK_LINK)

            f.filename = SAVE_PATH + uuid4().hex + '.jpg'
            f.save(f.filename)
            fs_n.append(f.filename)

        X = merger_v2.Merging(mode, fs_n, SAVE_PATH+dst, rows)
        if X != 0:
            return "<h3>Error occured!</h3><br>{}".format(GO_BACK_LINK)

        return render_template('result.html', img=dst)

if __name__ == '__main__':
    app.run(debug=True)