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
        
        print('[.]rows: {}'.format(rows))
        print('[.]Mode: _{}_'.format(mode))

        if mode == 'cs':
            if rows > len(file_list):
                return "Too many rows, sorry!<br>{}".format(GO_BACK_LINK)

        dst = uuid4().hex + '.jpg'
        fs_n = []
        for f in file_list:
            print(f.content_type)
            if f.content_type not in ALLOWED_MIME:
                return "Please upload png & jpg only!<br>{}".format(GO_BACK_LINK)

            f.filename = SAVE_PATH + uuid4().hex + '.jpg'
            f.save(f.filename)
            fs_n.append(f.filename)

        X = merger_v2.Merging(mode, fs_n, SAVE_PATH+dst, rows)
        if X != 'Success':
            return "Error occured!<br>{}".format(GO_BACK_LINK)

        return render_template('result.html', img=dst)

if __name__ == '__main__':
    app.run(debug=True)