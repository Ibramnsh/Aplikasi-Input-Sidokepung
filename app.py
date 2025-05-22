from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Buat folder static jika belum ada
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Simpan file Excel di folder static
EXCEL_FILENAME = 'data.xlsx'
EXCEL_FILE = os.path.join(STATIC_FOLDER, EXCEL_FILENAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        rt_rw_dusun = request.form.get('rt_rw_dusun')
        nama_kepala = request.form.get('nama_kepala')
        alamat = request.form.get('alamat')
        
        # Validasi data
        if not rt_rw_dusun or not nama_kepala or not alamat:
            return jsonify({'success': False, 'message': 'Semua field harus diisi'}), 400
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Data baru untuk ditambahkan
        new_data = {
            'Timestamp': timestamp,
            'RT/RW Dusun': rt_rw_dusun,
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
            
            # Tampilkan lokasi file untuk debugging
            file_location = f"File disimpan di: {EXCEL_FILE}"
            print(file_location)
            
            return jsonify({
                'success': True, 
                'message': 'Data berhasil disimpan',
                'file_location': file_location,
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
        download_name=f"data_keluarga_{datetime.now().strftime('%d%m%Y_%H%M%S')}.xlsx"
    )

@app.route('/file-location')
def file_location():
    """Menampilkan lokasi file Excel untuk memudahkan pengguna menemukan file"""
    return jsonify({'file_location': EXCEL_FILE})

if __name__ == '__main__':
    print(f"Data akan disimpan di: {EXCEL_FILE}")
    app.run(debug=True)