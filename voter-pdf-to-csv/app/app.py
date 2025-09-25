from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from pdf_processor import extract_voter_data
import pandas as pd
import tempfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process PDF and extract data
            voter_data = extract_voter_data(filepath)
            
            if not voter_data:
                return jsonify({'error': 'No data extracted from PDF'}), 400
            
            # Create CSV file
            df = pd.DataFrame(voter_data)
            
            # Create temporary CSV file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8-sig') as tmp_file:
                df.to_csv(tmp_file.name, index=False, encoding='utf-8-sig')
                csv_filename = filename.replace('.pdf', '_converted.csv')
                
                return jsonify({
                    'success': True,
                    'filename': csv_filename,
                    'download_url': f'/download/{os.path.basename(tmp_file.name)}'
                })
                
        except Exception as e:
            return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            filename,
            as_attachment=True,
            download_name=f'voter_list_converted.csv',
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
