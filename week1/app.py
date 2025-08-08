from flask import Flask, render_template, request, redirect, flash
import redis
import os
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = 'simple-secret-key'

def connect_redis():
    try:
        # Baca password Redis dari Docker Secret atau environment
        redis_password = 'defaultpassword'  # untuk fallback
        try:
            with open('/run/secrets/redis_password', 'r') as f:
                redis_password = f.read().strip()
        except:
            # cari di environment variable (klo ada)
            redis_password = os.environ.get('REDIS_PASSWORD', 'defaultpassword')
        
        r = redis.Redis(
            host='redis',
            port=6379,
            password=redis_password,
            decode_responses=True
        )
        r.ping()  # Test koneksi
        return r
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_message():
    name = request.form.get('name')
    message = request.form.get('message')
    
    if name and message:
        # Simpan ke Redis
        r = connect_redis()
        if r:
            # Buat data pesan
            wib = pytz.timezone('Asia/Jakarta')
            now_wib = datetime.now(wib)
            data = f"{now_wib.strftime('%Y-%m-%d %H:%M:%S WIB')} - {name}: {message}"
            r.lpush('messages', data)  # Simpan ke Redis list
            flash('Pesan berhasil disimpan!', 'success')
        else:
            flash('Gagal terhubung ke Redis!', 'error')
    else:
        flash('Nama dan pesan harus diisi!', 'error')
    
    return redirect('/')

@app.route('/messages')
def view_messages():
    r = connect_redis()
    messages = []
    if r:
        # get 10 pesan terakhir dari Redis
        messages = r.lrange('messages', 0, 9)
    
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)