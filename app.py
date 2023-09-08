from flask import Flask, render_template, request, redirect, url_for, send_file
import tempfile
from pdf2docx import Converter

app = Flask(__name__)

# Configure a temporary directory to store uploaded files
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

# Function to convert PDF to Word
def convert_pdf_to_word(pdf_file):
    temp_word_file = tempfile.mktemp(suffix=".docx")
    cv = Converter(pdf_file)
    cv.convert(temp_word_file, start=0, end=None)
    cv.close()
    return temp_word_file

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling file upload and conversion
@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return redirect(request.url)

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return redirect(request.url)

    if pdf_file:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(pdf_path)

        word_file = convert_pdf_to_word(pdf_path)
        
        return send_file(word_file, as_attachment=True)
    
    return 'Conversion failed'

if __name__ == '__main__':
    app.run(debug=True)

