from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from pdf2docx import Converter
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pdf_to_word', methods=['POST'])
def pdf_to_word():
    data = request.get_json()
    file_url = data.get('file_url')
    if not file_url:
        return {'error': 'No file_url provided'}, 400
    
@app.route('/pdf_to_word', methods=['GET', 'POST'])
def pdf_to_word():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('pdf_to_word.html', error='No file part')

        file = request.files['file']
        if file.filename == '':
            return render_template('pdf_to_word.html', error='No selected file')

        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Convert PDF to Word
            word_filename = os.path.join(app.config['CONVERTED_FOLDER'], file.filename.replace('.pdf', '.docx'))
            cv = Converter(filename)
            cv.convert(word_filename, start=0, end=None)
            cv.close()

            # Return the converted Word file for download
            return send_file(word_filename, as_attachment=True)

    return render_template('pdf_to_word.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)