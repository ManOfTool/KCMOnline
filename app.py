from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from uuid import uuid4
import merger_v2
app = Flask(__name__)

SAVE_PATH = 'static/images/'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        mode = request.form['mode']
        file_list = request.files.getlist('file')
        dst = uuid4().hex + '.jpg'
        fs_n = []
        for f in file_list:
            if f.filename.split('.')[-1].lower() not in ['jpg', 'png', 'jpeg']:
                return redirect(url_for('upload_file'))

            f.save(SAVE_PATH + secure_filename(f.filename))
            fs_n.append(SAVE_PATH + secure_filename(f.filename))

        X = merger_v2.Merging(mode, fs_n, SAVE_PATH+dst)
        if X != 'Success':
            return redirect(url_for('upload_file'))

        return render_template('result.html', img=dst)

if __name__ == '__main__':
    app.run(debug=True)