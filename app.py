from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
os.makedirs(STATIC_FOLDER, exist_ok=True)

EXCEL_FILENAME = 'data.xlsx'
EXCEL_FILE = os.path.join(STATIC_FOLDER, EXCEL_FILENAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        rt = request.form.get('rt')
        rw = request.form.get('rw')
        dusun = request.form.get('dusun')
        nama_kepala = request.form.get('nama_kepala')
        alamat = request.form.get('alamat')
        
        # Validasi data
        if not rt or not rw or not dusun or not nama_kepala or not alamat:
            return jsonify({'success': False, 'message': 'Semua field harus diisi'}), 400
        
        # Tambahkan timestamp
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Data baru untuk ditambahkan
        new_data = {
            'Timestamp': timestamp,
            'RT': rt,
            'RW': rw,
            'Dusun': dusun,
            'Nama Kepala Keluarga': nama_kepala,
            'Alamat': alamat
        }
        
        try:
            if os.path.exists(EXCEL_FILE):
                try:
                    df = pd.read_excel(EXCEL_FILE)
                    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                except PermissionError:
                    return jsonify({
                        'success': False, 
                        'message': 'File Excel sedang digunakan oleh program lain. Tutup file dan coba lagi.'
                    }), 500
            else:
                df = pd.DataFrame([new_data])
            
            df.to_excel(EXCEL_FILE, index=False)
            
            return jsonify({
                'success': True, 
                'message': 'Data berhasil disimpan',
                'download_url': f'/download/{EXCEL_FILENAME}'
            })
            
        except PermissionError as pe:
            error_msg = f"Permission denied: {str(pe)}. Pastikan folder memiliki izin tulis dan file tidak sedang dibuka."
            print(error_msg)
            return jsonify({'success': False, 'message': error_msg}), 500
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        return jsonify({'success': False, 'message': error_msg}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Route untuk mendownload file Excel"""
    return send_from_directory(
        directory=STATIC_FOLDER, 
        path=filename,
        as_attachment=True,
        download_name=f"data_keluarga_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

@app.route('/check-file')
def check_file():
    """Memeriksa apakah file Excel sudah ada"""
    exists = os.path.exists(EXCEL_FILE)
    return jsonify({'exists': exists})

if __name__ == '__main__':
    app.run(debug=True)