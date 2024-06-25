from flask import Flask, render_template, request, send_file
import os
from pdf2docx import Converter
from urllib.request import urlopen
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
    
    try:
        # Download the PDF file from the provided URL
        pdf_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.pdf')
        with urlopen(file_url) as response, open(pdf_filename, 'wb') as out_file:
            out_file.write(response.read())
        
        # Convert PDF to Word
        word_filename = os.path.join(app.config['CONVERTED_FOLDER'], 'converted.docx')
        cv = Converter(pdf_filename)
        cv.convert(word_filename, start=0, end=None)
        cv.close()

        # Return the converted Word file for download
        return send_file(word_filename, as_attachment=True)

    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
