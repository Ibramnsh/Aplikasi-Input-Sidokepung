from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
import pandas as pd
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Buat folder static/Excel jika belum ada
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/Excel')
os.makedirs(STATIC_FOLDER, exist_ok=True)

EXCEL_FILENAME = 'data_sensus.xlsx'
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
        jumlah_anggota = request.form.get('jumlah_anggota')
        jumlah_anggota_15plus = request.form.get('jumlah_anggota_15plus')
        
        # Validasi data di server
        if not rt or not rw or not dusun or not nama_kepala or not alamat or not jumlah_anggota or not jumlah_anggota_15plus:
            return jsonify({'success': False, 'message': 'Semua field harus diisi'}), 400
        
        # Konversi ke integer
        try:
            jumlah_anggota = int(jumlah_anggota)
            jumlah_anggota_15plus = int(jumlah_anggota_15plus)
        except ValueError:
            return jsonify({'success': False, 'message': 'Jumlah anggota harus berupa angka'}), 400
        
        # Validasi jumlah anggota
        if jumlah_anggota < 1:
            return jsonify({'success': False, 'message': 'Jumlah anggota keluarga minimal 1'}), 400
        
        if jumlah_anggota_15plus < 0:
            return jsonify({'success': False, 'message': 'Jumlah anggota usia 15+ tidak boleh negatif'}), 400
            
        if jumlah_anggota_15plus > jumlah_anggota:
            return jsonify({'success': False, 'message': 'Jumlah anggota usia 15+ tidak boleh lebih dari jumlah anggota keluarga'}), 400
        
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        keluarga_id = f"KEL-{rt}{rw}-{datetime.now().strftime('%d%m%Y%H%M%S')}"
        
        # Data baru untuk ditambahkan (baris pertama untuk kepala keluarga)
        new_data = {
            'Timestamp': timestamp,
            'ID Keluarga': keluarga_id,
            'RT': rt,
            'RW': rw,
            'Dusun': dusun,
            'Nama Kepala Keluarga': nama_kepala,
            'Alamat': alamat,
            'Jumlah Anggota Keluarga': jumlah_anggota,
            'Jumlah Anggota Usia 15+': jumlah_anggota_15plus,
            'Anggota Ke': 1, 
            'Nama Anggota': nama_kepala,
            'Umur': '', 
            'Hubungan dengan Kepala Keluarga': 'Kepala Keluarga',
            'Jenis Kelamin': '', 
            'Status Perkawinan': '',  
            'Pendidikan Terakhir': '',  
            'Kegiatan Sehari-hari': '',
            'Bekerja Untuk Upah': '',
            'Menjalankan Usaha': '',
            'Membantu Usaha Keluarga': '',
            'Memiliki Pekerjaan Tapi Sedang Tidak Bekerja': '',
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
                # Buat DataFrame baru jika file belum ada
                df = pd.DataFrame([new_data])
            
            # Simpan ke Excel
            df.to_excel(EXCEL_FILE, index=False)
            
            # Jika jumlah anggota usia 15+ lebih dari 0, redirect ke halaman lanjutan
            if jumlah_anggota_15plus > 0:
                # Simpan data ke session
                session['keluarga_data'] = {
                    'keluarga_id': keluarga_id,
                    'rt': rt,
                    'rw': rw,
                    'dusun': dusun,
                    'nama_kepala': nama_kepala,
                    'alamat': alamat,
                    'jumlah_anggota': jumlah_anggota,
                    'jumlah_anggota_15plus': jumlah_anggota_15plus,
                    'anggota_count': 1
                }
                
                return jsonify({
                    'success': True,
                    'redirect': True,
                    'redirect_url': url_for('lanjutan')
                })
            
            # Jika tidak ada anggota usia 15+, kembalikan respons normal
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

@app.route('/lanjutan')
def lanjutan():
    # Cek apakah ada data keluarga di session
    if 'keluarga_data' not in session:
        return redirect(url_for('index'))
    
    keluarga_data = session['keluarga_data']
    return render_template('lanjutan.html', keluarga_data=keluarga_data)

@app.route('/pekerjaan')
def pekerjaan():
    # Cek apakah ada data keluarga dan individu di session
    if 'keluarga_data' not in session or 'individu_data' not in session:
        return redirect(url_for('index'))
    
    keluarga_data = session['keluarga_data']
    individu_data = session['individu_data']
    return render_template('pekerjaan.html', keluarga_data=keluarga_data, individu_data=individu_data)


@app.route('/submit-individu', methods=['POST'])
def submit_individu():
    try:
        if 'keluarga_data' not in session:
            return jsonify({'success': False, 'message': 'Data keluarga tidak ditemukan'}), 400
        
        keluarga_data = session['keluarga_data']
        
        # Collect individu data from form
        nama = request.form.get('nama')
        umur = request.form.get('umur')
        hubungan = request.form.get('hubungan')
        jenis_kelamin = request.form.get('jenis_kelamin')
        status_perkawinan = request.form.get('status_perkawinan')
        pendidikan = request.form.get('pendidikan')
        kegiatan = request.form.get('kegiatan')
        bekerja_upah = request.form.get('bekerja_upah')
        menjalankan_usaha = request.form.get('menjalankan_usaha')
        membantu_usaha = request.form.get('membantu_usaha')
        memiliki_pekerjaan = request.form.get('memiliki_pekerjaan')
        
        # Validate individu data
        required_fields = [nama, umur, hubungan, jenis_kelamin, status_perkawinan, pendidikan, kegiatan, bekerja_upah, menjalankan_usaha, membantu_usaha]
        if not all(required_fields):
            return jsonify({'success': False, 'message': 'Semua field harus diisi'}), 400
        
        if bekerja_upah == 'Tidak' and menjalankan_usaha == 'Tidak' and membantu_usaha == 'Tidak' and not memiliki_pekerjaan:
            return jsonify({'success': False, 'message': 'Pertanyaan 5.10 harus dijawab'}), 400
        
        try:
            umur_int = int(umur)
        except ValueError:
            return jsonify({'success': False, 'message': 'Usia harus berupa angka'}), 400
        
        if umur_int < 15:
            return jsonify({'success': False, 'message': 'Usia minimal 15 tahun'}), 400
        
        # Increment anggota_count
        keluarga_data['anggota_count'] = keluarga_data.get('anggota_count', 0) + 1
        session['keluarga_data'] = keluarga_data
        
        # Store individu data temporarily in session (to combine later)
        session['individu_data'] = {
            'Nama Anggota': nama,
            'Umur': umur_int,
            'Hubungan dengan Kepala Keluarga': hubungan,
            'Jenis Kelamin': jenis_kelamin,
            'Status Perkawinan': status_perkawinan,
            'Pendidikan Terakhir': pendidikan,
            'Kegiatan Sehari-hari': kegiatan,
            'Bekerja Untuk Upah': bekerja_upah,
            'Menjalankan Usaha': menjalankan_usaha,
            'Membantu Usaha Keluarga': membantu_usaha,
            'Memiliki Pekerjaan Tapi Sedang Tidak Bekerja': memiliki_pekerjaan or '',
            'Anggota Ke': keluarga_data['anggota_count'],
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Always redirect to pekerjaan input after individu submission
        return jsonify({
            'success': True,
            'message': 'Data individu berhasil disimpan di sesi. Silakan lanjutkan input pekerjaan.',
            'redirect_to_pekerjaan': True,
            'redirect_url': url_for('pekerjaan') 
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/submit-pekerjaan', methods=['POST'])
def submit_pekerjaan():
    try:
        if 'keluarga_data' not in session:
            return jsonify({'success': False, 'message': 'Data keluarga tidak ditemukan'}), 400
        
        if 'individu_data' not in session:
            return jsonify({'success': False, 'message': 'Data individu tidak ditemukan, submit individu terlebih dahulu'}), 400
        
        keluarga_data = session['keluarga_data']
        individu_data = session['individu_data']
        
        # Collect pekerjaan data from form
        status_pekerjaan = request.form.get('status_pekerjaan')
        pemasaran_usaha = request.form.get('pemasaran_usaha')
        penjualan_marketplace = request.form.get('penjualan_marketplace')
        status_pekerjaan_diinginkan = request.form.get('status_pekerjaan_diinginkan')
        bidang_usaha = request.form.get('bidang_usaha')
        lebih_dari_satu_usaha = request.form.get('lebih_dari_satu_pekerjaan')
        
        required_pekerjaan_fields = [status_pekerjaan, pemasaran_usaha, penjualan_marketplace, status_pekerjaan_diinginkan, bidang_usaha, lebih_dari_satu_usaha]
        if not all(required_pekerjaan_fields):
            return jsonify({'success': False, 'message': 'Semua field pekerjaan harus diisi'}), 400
        
        # Combine individu data and pekerjaan data
        combined_data = {
            'ID Keluarga': keluarga_data['keluarga_id'],
            'RT': keluarga_data['rt'],
            'RW': keluarga_data['rw'],
            'Dusun': keluarga_data['dusun'],
            'Nama Kepala Keluarga': keluarga_data['nama_kepala'],
            'Alamat': keluarga_data['alamat'],
            'Jumlah Anggota Keluarga': keluarga_data['jumlah_anggota'],
            'Jumlah Anggota Usia 15+': keluarga_data['jumlah_anggota_15plus'],
        }
        combined_data.update(individu_data)
        combined_data.update({
            'Status Pekerjaan': status_pekerjaan,
            'Pemasaran Usaha': pemasaran_usaha,
            'Penjualan Marketplace': penjualan_marketplace,
            'Status Pekerjaan Diinginkan': status_pekerjaan_diinginkan,
            'Bidang Usaha': bidang_usaha,
            'Lebih dari Satu Usaha': lebih_dari_satu_usaha,
        })
        
        # Save combined data to Excel
        if os.path.exists(EXCEL_FILE):
            try:
                df = pd.read_excel(EXCEL_FILE)
                df = pd.concat([df, pd.DataFrame([combined_data])], ignore_index=True)
            except PermissionError:
                return jsonify({
                    'success': False,
                    'message': 'File Excel sedang digunakan oleh program lain. Tutup file dan coba lagi.'
                }), 500
        else:
            df = pd.DataFrame([combined_data])
        
        df.to_excel(EXCEL_FILE, index=False)
        
        # Decrement anggota usia 15+
        keluarga_data['jumlah_anggota_15plus'] -= 1
        session['keluarga_data'] = keluarga_data
        
        # Remove individu data from session now that pekerjaan is done
        session.pop('individu_data', None)
        
        # Redirect logic
        if keluarga_data['jumlah_anggota_15plus'] > 0:
            return redirect(url_for('lanjutan'))  # Continue to next input
        else:
            # Clear keluarga data when finished
            session.pop('keluarga_data', None)
            return redirect(url_for('index'))  # Main page after all done

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500



@app.route('/download/<filename>')
def download_file(filename):
    """Route untuk mendownload file Excel"""
    try:
        # Pastikan filename adalah file yang diizinkan
        if filename != EXCEL_FILENAME:
            return "File tidak ditemukan", 404
        
        file_path = os.path.join(STATIC_FOLDER, filename)
        
        # Pastikan file ada
        if not os.path.exists(file_path):
            return "File tidak ditemukan", 404
        
        # Tentukan nama file yang akan didownload
        download_name = f"data_sensus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        return send_from_directory(
            directory=STATIC_FOLDER, 
            path=filename,
            as_attachment=True,
            download_name=download_name
        )
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/check-file')
def check_file():
    """Memeriksa apakah file Excel sudah ada"""
    exists = os.path.exists(EXCEL_FILE)
    return jsonify({'exists': exists})

if __name__ == '__main__':
    app.run(debug=True)
