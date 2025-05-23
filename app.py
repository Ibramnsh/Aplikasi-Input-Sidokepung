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
            'Lapangan Pekerjaan': '',
            'Status Pekerjaan': '',
            'Pendapatan per Bulan': ''
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
        # Cek apakah ada data keluarga di session
        if 'keluarga_data' not in session:
            return jsonify({'success': False, 'message': 'Data keluarga tidak ditemukan'}), 400
        
        keluarga_data = session['keluarga_data']
        
        # Ambil data dari form
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
        
        # Cek apakah perlu redirect ke halaman pekerjaan
        need_redirect = bekerja_upah == 'Ya' or menjalankan_usaha == 'Ya' or membantu_usaha == 'Ya'
        
        # Validasi data
        if not nama or not umur or not hubungan or not jenis_kelamin or not status_perkawinan or not pendidikan or not kegiatan or not bekerja_upah or not menjalankan_usaha or not membantu_usaha:
            return jsonify({'success': False, 'message': 'Semua field harus diisi'}), 400
        
        # Validasi pertanyaan 5.10 jika semua jawaban 5.7, 5.8, 5.9 adalah "Tidak"
        if bekerja_upah == 'Tidak' and menjalankan_usaha == 'Tidak' and membantu_usaha == 'Tidak' and not memiliki_pekerjaan:
            return jsonify({'success': False, 'message': 'Pertanyaan 5.10 harus dijawab'}), 400
        
        # Konversi usia ke integer
        try:
            umur = int(umur)
        except ValueError:
            return jsonify({'success': False, 'message': 'Usia harus berupa angka'}), 400
        
        # Validasi usia
        if umur < 15:
            return jsonify({'success': False, 'message': 'Usia minimal 15 tahun'}), 400
        
        # Tambahkan timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Increment anggota counter
        keluarga_data['anggota_count'] += 1
        
        # Data baru untuk ditambahkan
        new_data = {
            'Timestamp': timestamp,
            'ID Keluarga': keluarga_data['keluarga_id'],
            'RT': keluarga_data['rt'],
            'RW': keluarga_data['rw'],
            'Dusun': keluarga_data['dusun'],
            'Nama Kepala Keluarga': keluarga_data['nama_kepala'],
            'Alamat': keluarga_data['alamat'],
            'Jumlah Anggota Keluarga': keluarga_data['jumlah_anggota'],
            'Jumlah Anggota Usia 15+': keluarga_data['jumlah_anggota_15plus'],
            'Anggota Ke': keluarga_data['anggota_count'],
            'Nama Anggota': nama,
            'Umur': umur,
            'Hubungan dengan Kepala Keluarga': hubungan,
            'Jenis Kelamin': jenis_kelamin,
            'Status Perkawinan': status_perkawinan,
            'Pendidikan Terakhir': pendidikan,
            'Kegiatan Sehari-hari': kegiatan,
            'Bekerja Untuk Upah': bekerja_upah,
            'Menjalankan Usaha': menjalankan_usaha,
            'Membantu Usaha Keluarga': membantu_usaha,
            'Memiliki Pekerjaan Tapi Sedang Tidak Bekerja': memiliki_pekerjaan or '',
            'Lapangan Pekerjaan': '',
            'Status Pekerjaan': '',
            'Pendapatan per Bulan': ''
        }
        
        try:
            # Cek apakah file Excel sudah ada
            if os.path.exists(EXCEL_FILE):
                try:
                    # Baca file yang sudah ada
                    df = pd.read_excel(EXCEL_FILE)
                    # Tambahkan data baru
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
            
            # Jika perlu redirect ke halaman pekerjaan
            if need_redirect:
                # Simpan data individu ke session
                session['individu_data'] = {
                    'nama': nama,
                    'anggota_ke': keluarga_data['anggota_count']
                }
                
                return jsonify({
                    'success': True,
                    'message': 'Data berhasil disimpan',
                    'redirect_to_pekerjaan': True,
                    'redirect_url': url_for('pekerjaan')
                })
            
            # Kurangi jumlah anggota 15+ yang tersisa
            keluarga_data['jumlah_anggota_15plus'] -= 1
            session['keluarga_data'] = keluarga_data
            
            # Jika semua anggota 15+ sudah diinput, hapus session dan redirect ke halaman utama
            if keluarga_data['jumlah_anggota_15plus'] <= 0:
                session.pop('keluarga_data', None)
                if 'individu_data' in session:
                    session.pop('individu_data', None)
                return jsonify({
                    'success': True,
                    'message': 'Semua data berhasil disimpan',
                    'complete': True,
                    'redirect_url': url_for('index')
                })
            
            # Jika masih ada anggota 15+ yang belum diinput
            return jsonify({
                'success': True,
                'message': f'Data berhasil disimpan. Tersisa {keluarga_data["jumlah_anggota_15plus"]} anggota yang perlu diinput',
                'remaining': keluarga_data['jumlah_anggota_15plus']
            })
            
        except PermissionError as pe:
            error_msg = f"Permission denied: {str(pe)}. Pastikan folder memiliki izin tulis dan file tidak sedang dibuka."
            print(error_msg)
            return jsonify({'success': False, 'message': error_msg}), 500
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        return jsonify({'success': False, 'message': error_msg}), 500

@app.route('/submit-pekerjaan', methods=['POST'])
def submit_pekerjaan():
    try:
        # Cek apakah ada data keluarga dan individu di session
        if 'keluarga_data' not in session or 'individu_data' not in session:
            return jsonify({'success': False, 'message': 'Data tidak ditemukan'}), 400
        
        keluarga_data = session['keluarga_data']
        individu_data = session['individu_data']
        
        # Ambil data dari form
        lapangan_pekerjaan = request.form.get('lapangan_pekerjaan')
        status_pekerjaan = request.form.get('status_pekerjaan')
        pendapatan = request.form.get('pendapatan')
        
        # Validasi data
        if not lapangan_pekerjaan or not status_pekerjaan or not pendapatan:
            return jsonify({'success': False, 'message': 'Semua field harus diisi'}), 400
        
        # Konversi pendapatan ke integer
        try:
            pendapatan = int(pendapatan)
        except ValueError:
            return jsonify({'success': False, 'message': 'Pendapatan harus berupa angka'}), 400
        
        try:
            # Baca file Excel yang sudah ada
            df = pd.read_excel(EXCEL_FILE)
            
            # Cari baris yang sesuai dengan anggota yang sedang diinput
            mask = (df['ID Keluarga'] == keluarga_data['keluarga_id']) & \
                   (df['Anggota Ke'] == individu_data['anggota_ke'])
            
            # Update data pekerjaan pada baris yang sesuai
            df.loc[mask, 'Lapangan Pekerjaan'] = lapangan_pekerjaan
            df.loc[mask, 'Status Pekerjaan'] = status_pekerjaan
            df.loc[mask, 'Pendapatan per Bulan'] = pendapatan
            
            # Simpan kembali ke Excel
            df.to_excel(EXCEL_FILE, index=False)
            
            # Hapus data individu dari session
            session.pop('individu_data', None)
            
            return jsonify({
                'success': True,
                'message': 'Data pekerjaan berhasil disimpan',
                'redirect_url': url_for('lanjutan')
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
